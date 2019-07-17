import json
import csv

main_url = "http://stat.gibdd.ru/"


def open_csv(link):
    with open(link, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)
        data.pop(0)
        return data


def open_json(path):
    with open(path) as data_file:
        data = json.load(data_file)

    return data


def save_json(data,path):
    with open(path, 'w') as data_file:
        json.dump(data, data_file, ensure_ascii=True)
