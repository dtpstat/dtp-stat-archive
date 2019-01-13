from dtp_parser import update_regions
from dtp_parser import update_dtp

import sys
import os
import warnings
import locale
import csv

import django
sys.path.append(os.path.join(os.path.dirname(__file__), '../dtpmap/dtpmap'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtpmap.settings")
django.setup()

locale.setlocale(locale.LC_TIME, "ru_RU")
warnings.filterwarnings('ignore')

from dtpmapapp import models
from django.shortcuts import get_object_or_404


def open_csv(link):
    with open(link, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
        data.pop(0)
        return data


def get_tech_data():
    for participant_type in open_csv("data/participant_types.csv"):
        try:
            get_object_or_404(models.MVCParticipantType,name=participant_type[0])
            continue
        except:
            participant_type_item = models.MVCParticipantType(
                name=participant_type[0],
                label=participant_type[1]
            )
            participant_type_item.save()


def get_regions():
    update_regions.main()


def get_data():
    update_dtp.main()


def load(data):
    if len(data) > 0:
        for item in data:
            if item == "tech_data":
                get_tech_data()
            elif item == "regions":
                get_regions()
            elif item == "data":
                get_data()
    else:
        get_tech_data()
        get_regions()
        get_data()


def main(args):
    load(args[1:])


if __name__ == "__main__":
    main(sys.argv)
