from dtp_parser.extra import main_url

import sys
import os
import warnings
import locale
import requests
from bs4 import BeautifulSoup
import json
import re
from tqdm import tqdm
from ast import literal_eval
from slugify import slugify

import django
sys.path.append(os.path.join(os.path.dirname(__file__), '../dtpmap/dtpmap'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtpmap.settings")
django.setup()

from dtpmapapp import models
from django.shortcuts import get_object_or_404

locale.setlocale(locale.LC_TIME, "ru_RU")
warnings.filterwarnings('ignore')


def geocoder(address):
    try:
        link = "https://geocode-maps.yandex.ru/1.x/?format=json&geocode=" + str(address)
        r = requests.get(link)
        if r.status_code != 200:
            return "Error"
        else:
            r = r.json()
            longitude = r['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')[0]
            latitude = r['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')[1]
        try:
            return latitude, longitude
        except:
            return None, None
    except:
        return None, None


def main():
    regions = {}

    # делаем запрос к stat.gibdd.ru
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # ищем скрипт с кодами ОКТМО регионов и выкачиваем их
    scripts = soup.find_all("script")

    for script in scripts:
        if script.string is not None and "downloadRegListData" in script.string:
            string = script.string
            p = re.compile(r"downloadRegListData = (.*?);", re.MULTILINE)
            m = p.search(string)
            data = m.groups()[0]
            jdata = json.loads(data)
            for federal_district in jdata[0]["Nodes"]:
                for region in federal_district["Nodes"]:
                    region_name = region['Text'].replace("г.","").replace("гор.","").strip()
                    regions[region_name] = {
                        "code": region['Value'],
                        "areas": []
                    }

    # делаем запросы по регионам и качаем коды ОКТМО для районов и городов
    for region in tqdm(list(regions.keys())):
        region_code = regions[region]['code']

        payload = {
            "maptype": 1,
            "region": region_code,
            "pok": "1"
        }

        area_request = requests.post("http://stat.gibdd.ru/map/getMainMapData", json=payload)
        area_response = area_request.json()['metabase']
        export = json.loads(literal_eval(area_response)[0]['maps'])
        for area in export:
            area_name = area["name"].replace("г.", "").replace("гор.", "").replace("ГО", "").strip()
            regions[region]['areas'].append({"area": area_name, "area_code": area["id"]})


    # записываем в базу
    for region in tqdm(list(regions.items())):
        try:
            region_item = get_object_or_404(models.Region, name=region[0], level=1)
        except:
            region_item=models.Region(
                name=region[0],
                oktmo_code=region[1]['code'],
                level=1,
                alias=slugify(region[0]),
                status=False
            )

        if region_item.latitude and region_item.longitude:
            pass
        else:
            region_item.latitude, region_item.longitude = geocoder(region_item.name)

        region_item.save()

        for area in region[1]['areas']:
            try:
                area_item = get_object_or_404(models.Region, oktmo_code=area['area_code'], name=area['area'], level=2)
            except:
                area_item = models.Region(
                    name=area['area'],
                    oktmo_code=area['area_code'],
                    level=2,
                    parent_region_id=region_item.id,
                    alias=slugify(area['area']),
                    status=True
                )

            if area_item.latitude and area_item.longitude:
                pass
            else:
                area_item.latitude, area_item.longitude = geocoder(area_item.parent_region.name + " " + area_item.name)

            area_item.save()
