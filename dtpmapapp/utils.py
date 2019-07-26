import zipfile
from dtpmapapp import models
import json
import os
import environ
env = environ.Env()

def save_json(data, path):
    with open(path, 'w') as data_file:
        json.dump(data, data_file, ensure_ascii=False)


def save_archive(path, import_file_name, export_file_name):
    os.chdir(path)
    with zipfile.ZipFile(export_file_name, "w", zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(import_file_name)


def create_dump(source=False):
    export_data = []

    for dtp in models.MVC.objects.all():
        last_source_code = models.SourceData.objects.filter(mvc=dtp).latest('date').data

        if source:
            pass
        else:
            last_source_code['infoDtp']['COORD_L'] = dtp.longitude
            last_source_code['infoDtp']['COORD_W'] = dtp.latitude

        export_data.append(last_source_code)

    if source:
        dump_name = 'source_dtp'
    else:
        dump_name = 'dtp'

    if env('DEBUG') == False:
        path = "static_root"
    else:
        path = "static"

    save_json(export_data, path + "/open_data/" + dump_name + ".json")
    save_archive(path + "/open_data/", dump_name + ".json", dump_name + ".json.zip")