#!/usr/bin/python
import requests
from tqdm import *
import csv

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
           'Accept': 'application/json, text/javascript, */*; q=0.01'}

start_url = 'https://russiaedu.ru/_ajax/schools?edu_school_filter%5BschoolName%5D=&edu_school_filter%5Bregion%5D=' \
      '&edu_school_filter%5Bdistrict%5D=&edu_school_filter%5BformType%5D=&edu_school_filter%5BownershipType%5D=' \
      '&edu_school_filter%5B_token%5D=mZ4TgkB-uxCGEws3rnAwECJLcbCLooAiS2kGOogr0cA&pp=1&pageNumber=1&direction='

json_ = requests.get(start_url, headers=headers)
pages = int(json_.json()['pageCount'])
base = [['Название школы', 'Директор', 'Адрес', 'Тип населенного пункта', 'Район', 'Регион', 'Телефон', 'Сайт', 'Email', 'Источник']]


def writing_raw(data):
    current = []
    current.append(data['data']['title'])
    current.append(data['data']['director'])
    current.append(data['data']['address'].strip())
    if 'г.' in data['data']['address'] or 'город' in data['data']['address']:
        current.append('Город')
    elif 'п.' in data['data']['address']:
        current.append('Посёлок')
    elif 'с.' in data['data']['address'] or 'село' in data['data']['address']:
        current.append('Село')
    elif 'п.г.т.' in data['data']['address'] or 'поселок городского типа' in data['data']['address']:
        current.append('Посёлок городского типа')
    elif 'д.' in data['data']['address'] or 'деревня' in data['data']['address']:
        current.append('Деревня')
    elif 'р.п.' in data['data']['address'] or 'рабочий посёлок' in data['data']['address']:
        current.append('Рабочий посёлок')
    else:
        current.append('Город')
    if 'район' in data['data']['address']:
        for i in data['data']['address'].split(','):
            if 'район' in i:
                current.append(i.strip())
    else:
        current.append(None)
    if 'область' in data['data']['address'] or 'обл' in data['data']['address'] or 'об' in data['data']['address']:
        for i in data['data']['address'].split(','):
            if 'область' in i or 'обл' in i or 'об' in i:
                current.append(i.strip())
    elif 'край' in data['data']['address']:
        for i in data['data']['address'].split(','):
            if 'край' in i:
                current.append(i.strip())
    elif 'Республика' in data['data']['address']:
        for i in data['data']['address'].split(','):
            if 'Республика' in i:
                current.append(i.strip())
    else:
        current.append(None)
    current.append(data['data']['phone'])
    current.append(data['data']['site'])
    current.append(data['data']['email'])
    current.append(f"https://russiaedu.ru{data['link']}")
    return current


print('Staring parse...')
with tqdm(total=pages // 10000 + 1) as pbar:
    for i in range(1, pages // 10000 + 2):
        url = f'https://russiaedu.ru/_ajax/schools?edu_school_filter%5BschoolName%5D=&edu_school_filter%5Bregion%' \
              f'5D=&edu_school_filter%5Bdistrict%5D=&edu_school_filter%5BformType%5D=&edu_school_filter%' \
              f'5BownershipType%5D=&edu_school_filter%5B_token%5D=mZ4TgkB-uxCGEws3rnAwECJLcbCLooAiS2kGOogr0cA&pp=' \
              f'10000&pageNumber={i}&direction='
        json_to_parse = requests.get(url, headers=headers)
        for data in json_to_parse.json()['eduSchools']:
            base.append(writing_raw(data))
        pbar.update()
print('Done!')
with open('base.csv', 'w') as f:
    w = csv.writer(f)
    w.writerows(base)
    f.close()
