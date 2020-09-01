#!/usr/bin/python
import requests
from tqdm import *
import csv
import json


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
           'Accept': 'application/json, text/javascript, */*; q=0.01'}

start_url = 'https://bus.gov.ru/public-rest/api/agency/search/init?d-442831-p=1&orderAttributeName=rank&' \
            'orderDirectionASC=false&pageSize=30&searchString=школа&searchTermCondition=or'
search_page = requests.get(start_url, headers=headers)
base = [['Название школы', 'Директор', 'Адрес', 'Тип населенного пункта', 'Регион', 'Телефон', 'Сайт', 'Email', 'Источник']]
current_pages = search_page.json()['agencies']
with open('regions.json', 'r', encoding='utf-8') as fh:
    data = json.load(fh)


def writing_raw(current_pages, region, id):
    for page in current_pages:
        page_url = f'https://bus.gov.ru/public/agency/agency.json?agency={id}'
        json_ = requests.get(page_url, headers=headers).json()
        name = page['shortName'].strip()
        address = page['fullAddress'].strip()
        loc_type = f"{json_['publicInfo']['ppo']['settlementType']}"
        region = region
        phone = page['phone'].strip()
        site = page['website'].strip()
        link = f"https://bus.gov.ru/pub/info-card/{str(page['agencyId'])}".strip()
        director = f"{json_['agency']['managerSecondName']} " \
                   f"{json_['agency']['managerFirstName']} {json_['agency']['managerMiddleName']}"
        email = f"{json_['agency']['email']}"
        return [name, director, address, loc_type, region, phone, site, email, link]


if __name__ == '__main__':
    print('Staring parse...')
    with tqdm(total=len(data)) as pbar:
        for reg, id in data.items():
            print(f'Working at {reg}...')
            for i in range(1, (int(id[1]) + 1) // 30 + 1):
                url = f'https://bus.gov.ru/public-rest/api/agency/search/init?d-442831-p={i}&orderAttributeName=rank&' \
                      f'orderDirectionASC=false&pageSize=30&regionId={str(id[0])}&regions={str(id[0])}&' \
                      f'searchString=школа&searchTermCondition=or'
                try:
                    json_to_parse = requests.get(url, headers=headers)
                    base.append(writing_raw(json_to_parse.json()['agencies'], reg, str(id[0])))
                except:
                    continue
            pbar.update()
            print()

    with open('base.csv', 'w') as f:
        w = csv.writer(f)
        w.writerows(base)
        f.close()

    print('Done!')
