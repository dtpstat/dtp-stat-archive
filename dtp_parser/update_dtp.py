import sys
import os
from tqdm import tqdm
import requests
from ast import literal_eval
from slugify import slugify
import geopy
import geopy.distance
import random

from datetime import datetime, timedelta

from dtp_parser.extra import main_url
from dtp_parser.geocoder_51c import Geocoder_51c

import django
sys.path.append(os.path.join(os.path.dirname(__file__), '../dtpmap/dtpmap'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtpmap.settings")
django.setup()

from dtpmapapp import models
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum, F

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


# сохраняем ДТП
def add_mvc(source_crash_data, area, types):

    try:
        mvc_item = get_object_or_404(models.MVC, alias=source_crash_data['KartId'])
    except:
        mvc_item = models.MVC()

    date_time = datetime.strptime(source_crash_data['date'] + " " + source_crash_data['Time'], '%d.%m.%Y %H:%M')

    if source_crash_data['DTP_V'] in types.keys():
        type_id = types.get(source_crash_data['DTP_V'])
    else:
        try:
            type_item = get_object_or_404(models.MVCType, name=source_crash_data['DTP_V'])
        except:
            type_item = models.MVCType(
                name=source_crash_data['DTP_V'],
                alias=slugify(source_crash_data['DTP_V'])
            )
            type_item.save()

        type_id = type_item.id

    mvc_item.region_id=area.id
    mvc_item.datetime=date_time
    mvc_item.type_id=type_id
    mvc_item.participants=source_crash_data['K_UCH']
    mvc_item.dead=source_crash_data['POG']
    mvc_item.injured=source_crash_data['RAN']
    mvc_item.alias=source_crash_data['KartId']
    mvc_item.scheme=source_crash_data['infoDtp']['s_dtp'] if source_crash_data['infoDtp']['s_dtp'] not in ["990", "390", "290", "490", "890","590","690","790"] else None
    mvc_item.source_data=source_crash_data
    mvc_item.conditions=get_conditions(source_crash_data)

    geo_data = update_geolocation(area, source_crash_data)
    mvc_item.street_id = geo_data['street_id']
    mvc_item.address = geo_data['address']
    mvc_item.latitude = geo_data['latitude']
    mvc_item.longitude = geo_data['longitude']
    mvc_item.geo_updated = geo_data['geo_updated']
    #mvc_item.geo_updated = False

    mvc_item.save()

    mvc_item.participant_set.clear()

    return mvc_item


# сохраняем улицы
def add_street(area, source_street):
    if source_street is None:
        return None
    else:
        try:
            street_item = get_object_or_404(models.Street, area=area, name=source_street)
        except:
            street_item = models.Street(
                name=source_street
            )
            street_item.save()

        return street_item.id


# сохраняем участников
def add_participant(mvc_item_id,ts_item_id,participant,offences):
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
            if offence in offences.keys():
                offence_id = offences.get(offence)
            else:
                try:
                    offence_item = get_object_or_404(models.Offence, name=offence)
                except:
                    offence_item = models.Offence(
                        name=offence
                    )
                    offence_item.save()

                offence_id = offence_item.id

            participant_item.offences.add(offence_id)


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
        geodata['address'] = ", ".join(source_road_components).strip()
    elif source_address_components[1] not in [None, ""]:
        geodata['street_id'] = add_street(area, source_data['infoDtp']['street'])
        geodata['address'] = ", ".join(source_address_components).strip()

        if len(geodata['address']) > 5:
            new_data = geocoder(source_address_components, source_coordinates)
            if new_data:
                geodata['latitude'] = new_data['latitude']
                geodata['longitude'] = new_data['longitude']
                geodata['geo_updated'] = True

    return geodata


# выгружаем данные
def get_crashes_data(area):
    dates = generate_dates_by_start_end(datetime(2015, 1, 1), datetime(datetime.now().year, datetime.now().month, 1))

    types = {x['name']:x['id'] for x in models.MVCType.objects.all().values('name','id')}
    nearby = {x['name']:x['id'] for x in models.Nearby.objects.all().values('name','id')}
    offences = {x['name']:x['id'] for x in models.Offence.objects.all().values('name','id')}
    participant_types = {x['name']:x['id'] for x in models.MVCParticipantType.objects.all().values('name','id')}

    area_crashes = []

    for date in tqdm(dates, leave=False, desc=area.name):
        payload = {}

        payload["data"] = '{"date":["MONTHS:' + date + '"],"ParReg":"' + area.parent_region.oktmo_code + '","order":{"type":"1","fieldName":"dat"},"reg":"' + area.oktmo_code + '","ind":"1","st":"1","en":"10000"}'

        response = requests.post(main_url + "map/getDTPCardData", json=payload)

        try:
            response = response.json()
            export = literal_eval(response['data'])
            area_crashes.extend(export['tab'])
        except:
            pass

    for local_crash in area_crashes:

        mvc_item = add_mvc(local_crash, area, types)

        for nearby_object in (local_crash['infoDtp']['OBJ_DTP'] + local_crash['infoDtp']['sdor']):
            if nearby_object != "Перегон (нет объектов на месте ДТП)" and nearby_object != "Отсутствие в непосредственной близости объектов УДС и объектов притяжения":
                if nearby_object in nearby.keys():
                    nearby_object_id = nearby.get(nearby_object)
                else:
                    try:
                        nearby_object_item = get_object_or_404(models.Nearby, name=nearby_object)
                    except:
                        nearby_object_item = models.Nearby(
                            name=nearby_object
                        )
                        nearby_object_item.save()

                    nearby_object_id = nearby_object_item.id

                mvc_item.nearby.add(nearby_object_id)

        participant_type_id = participant_types.get("auto")

        for ts in local_crash['infoDtp']['ts_info']:
            ts_item = add_ts(ts)

            for participant in ts['ts_uch']:
                add_participant(mvc_item.id, ts_item.id, participant,offences)
                if "вело" in participant['K_UCH'].lower():
                    participant_type_id = participant_types.get("bicycle")

        for participant in local_crash['infoDtp']['uchInfo']:
            add_participant(mvc_item.id, None, participant,offences)
            if participant_type_id != participant_types.get("bicycle"):
                participant_type_id = participant_types.get("pedestrian")

        mvc_item.participant_type_id=participant_type_id
        mvc_item.save()

    #update_geolocation(area, dates)


# проверяем дубликаты координат
def check_coordinates_duplicates():
    duplicates_values = models.MVC.objects.values('longitude', 'latitude').annotate(Count('id')).order_by().filter(id__count__gt=1)
    duplicates = models.MVC.objects.filter(longitude__in=[item['longitude'] for item in duplicates_values],latitude__in=[item['latitude'] for item in duplicates_values])

    d = geopy.distance.vincenty(meters=10)
    for mvc in duplicates:
        start = geopy.Point(mvc.latitude, mvc.longitude)
        new_point = d.destination(point=start, bearing=random.randint(0,360))
        mvc.longitude = new_point.longitude
        mvc.latitude = new_point.latitude
        mvc.save()


def main():
    regions = models.Region.objects.filter(level__exact=2, status=True)

    for area in tqdm(regions, desc="Выгрузка ДТП", leave=False):
        if area.oktmo_code == "33250":
            get_crashes_data(area)

    check_coordinates_duplicates()

