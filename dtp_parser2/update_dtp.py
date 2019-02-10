import sys
import os
from slugify import slugify
import ijson
from tqdm import tqdm

from datetime import datetime, timedelta

from dtp_parser.geocoder_51c import Geocoder_51c

import django
sys.path.append(os.path.join(os.path.dirname(__file__), '../dtpmap/dtpmap'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtpmap.settings")
django.setup()

from django.db import transaction

from dtpmapapp import models
from django.shortcuts import get_object_or_404

api = Geocoder_51c()


# генерируем даты
def generate_dates_by_start_end(start, end):
    date_list = [start]

    while start < end:
        start += timedelta(days=32)
        start = start.replace(day=1)
        date_list.append(datetime(start.year, start.month, 1))

    return [x.strftime('%m.%Y') for x in date_list]


# выгружаем условия, в которых произошло ДТП
def get_conditions(local_crash):
    conditions = []

    for i in (local_crash['infoDtp']['ndu'] + local_crash['infoDtp']['s_pog']):
        if i != "Не установлены":
            conditions.append(i)

    conditions.append(local_crash['infoDtp']['osv'])
    conditions.append("Покрытие – " + local_crash['infoDtp']['s_pch'].lower())

    return conditions


def get_type_id(type_name):
    type_item, created = models.MVCType.objects.get_or_create(
        name=type_name
    )
    if created:
        type_item.alias = slugify(type_name)

    return type_item.id


# сохраняем ДТП
def add_dtp(source_crash_data):

    area = get_object_or_404(models.Region, oktmo_code=source_crash_data["oktmo_code"], parent_region__oktmo_code=source_crash_data["parent_region_code"])

    mvc_item, created = models.MVC.objects.get_or_create(
        alias=source_crash_data['KartId']
    )

    date_time = datetime.strptime(source_crash_data['date'] + " " + source_crash_data['Time'], '%d.%m.%Y %H:%M')

    mvc_item.region_id=area.id
    mvc_item.datetime=date_time
    mvc_item.type_id=get_type_id(source_crash_data['DTP_V'])
    mvc_item.participants=source_crash_data['K_UCH']
    mvc_item.dead=source_crash_data['POG']
    mvc_item.injured=source_crash_data['RAN']
    mvc_item.alias=source_crash_data['KartId']
    mvc_item.scheme=source_crash_data['infoDtp']['s_dtp'] if source_crash_data['infoDtp']['s_dtp'] not in ["290", "390", "490", "590", "690", "790", "890", "990"] else None
    mvc_item.conditions=get_conditions(source_crash_data)

    geo_data = update_geolocation(area, source_crash_data)
    mvc_item.street_id = geo_data['street_id']
    mvc_item.address = geo_data['address']
    mvc_item.latitude = geo_data['latitude']
    mvc_item.longitude = geo_data['longitude']
    mvc_item.geo_updated = geo_data['geo_updated']

    mvc_item.save()

    source_data_item = models.SourceData(
        mvc=mvc_item,
        data=source_crash_data
    )
    source_data_item.save()

    mvc_item.participant_set.clear()

    return mvc_item


# сохраняем улицы
def add_street(area, source_street):
    if source_street is None:
        return None
    else:
        street_item, created = models.Street.objects.get_or_create(
            name=source_street
        )
        return street_item.id


# сохраняем участников
def add_participant(mvc_item_id,ts_item_id,participant):
    if participant['POL'] == "Мужской":
        gender = "мужчина"
    elif participant['POL'] == "Женский":
        gender = "женщина"
    else:
        gender = None

    participant_item = models.Participant(
        role=participant['K_UCH'],
        driving_experience=participant['V_ST'] if participant['V_ST'] != "" else None,
        status=participant['S_T'],
        gender=gender,
        abscond=participant['S_SM'],
        mvc_id=mvc_item_id,
        car_id=ts_item_id
    )

    participant_item.save()

    for offence in (participant['NPDD'] + participant['NPDD']):
        if offence != "Нет нарушений":
            offence_item, created = models.Offence.objects.get_or_create(
                name=offence
            )
            participant_item.offences.add(offence_item)


# сохраняем транспортные средства
def add_ts(ts):

    if "прочие" in ts['m_ts'].lower() or ts['m_ts'] == "":
        car_model = None
    else:
        car_model = ts['m_ts'].strip()

    if "Прочие марки мотоциклов" in ts['marka_ts']:
        brand = "Мотоцикл"
    elif ts['marka_ts'] == "":
        brand = None
    else:
        brand = ts['marka_ts'].strip()

    ts_item = models.Car(
        brand=brand,
        car_model=car_model,
        manufacture_year=ts['g_v'] if ts['g_v'] != "" else None,
        color=ts['color']
    )

    ts_item.save()

    return ts_item


# геокодируем адреса
def geocoder(address_components, coordinates):
    try:
        geo_data = eval(api.get_correct_point(address_components[0], address_components[1], address_components[2], [coordinates[0], coordinates[1]]))
        return {'latitude': geo_data['result'][0], 'longitude': geo_data['result'][1]}
    except:
        return None


# обрабатываем адреса и координаты
def update_geolocation(area, source_data):
    try:
        source_coordinates = [float(source_data['infoDtp']['COORD_W']), float(source_data['infoDtp']['COORD_L'])]
    except:
        source_coordinates = [0, 0]

    source_address_components = [source_data['infoDtp']['n_p'], source_data['infoDtp']['street'], source_data['infoDtp']['house']]
    source_road_components = [source_data['infoDtp']['n_p'], source_data['infoDtp']['dor']]

    geodata = {
        "address": None,
        "street_id": None,
        "latitude": source_coordinates[0],
        "longitude": source_coordinates[1],
        "geo_updated": False
    }

    if source_road_components[1] not in [None, ""]:
        geodata['street_id'] = add_street(area, source_data['infoDtp']['dor'])
        geodata['address'] = ", ".join([x for x in source_road_components if x]).strip()
    elif source_address_components[1] not in [None, ""]:
        geodata['street_id'] = add_street(area, source_data['infoDtp']['street'])
        geodata['address'] = ", ".join([x for x in source_address_components if x]).strip()

        """
        if len(geodata['address']) > 5:
            new_data = geocoder(source_address_components, source_coordinates)
            if new_data:
                geodata['latitude'] = new_data['latitude']
                geodata['longitude'] = new_data['longitude']
                geodata['geo_updated'] = True
        """

    return geodata


# выгружаем данные
def get_crashes_data(dtp):

    last_source_code = models.SourceData.objects.filter(mvc__alias=dtp['KartId'])

    if len(last_source_code)>0 and last_source_code.latest('date').data == dtp:
        return
    else:
        mvc_item = add_dtp(dtp)

        for nearby_object in (dtp['infoDtp']['OBJ_DTP'] + dtp['infoDtp']['sdor']):
            if nearby_object != "Перегон (нет объектов на месте ДТП)" and nearby_object != "Отсутствие в непосредственной близости объектов УДС и объектов притяжения":
                nearby_object_item, created = models.Nearby.objects.get_or_create(
                    name=nearby_object
                )

                mvc_item.nearby.add(nearby_object_item.id)

        participant_types = {x['name']:x['id'] for x in models.MVCParticipantType.objects.all().values("name","id")}
        participant_type_id = participant_types.get("auto")

        for ts in dtp['infoDtp']['ts_info']:
            ts_item = add_ts(ts)

            for participant in ts['ts_uch']:
                add_participant(mvc_item.id, ts_item.id, participant)
                if "вело" in participant['K_UCH'].lower():
                    participant_type_id = participant_types.get("bicycle")

        for participant in dtp['infoDtp']['uchInfo']:
            add_participant(mvc_item.id, None, participant)
            if participant_type_id != participant_types.get("bicycle"):
                participant_type_id = participant_types.get("pedestrian")

        mvc_item.participant_type_id=participant_type_id
        mvc_item.save()


def main():
    with open("data/dtp.json", 'r') as f:
        objects = ijson.items(f, 'item')
        for row in tqdm(objects):
            get_crashes_data(row)
