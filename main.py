#!/usr/bin/python
import grequests
from tqdm import tqdm
import csv
from preapre import *
import requests


with open('bad_schools.txt', 'r', encoding='utf-8') as fil:
    bad_schools = fil.read().split('\n')

with open('bad_knots.txt', 'r', encoding='utf-8') as files:
    bad_knots = files.read().split('\n')


def parsing():
    base = [['Наименование', 'Директор', 'Адрес', 'Тип населённого пункта',
             'Регион', 'Телефон', 'Сайт', 'E-mail', 'Источник']]
    print('Начинаем работу...')
    for reg in tqdm(DATA.keys(), position=0, leave=True):
        region = Region(reg)
        for knot in tqdm(
                grequests.map(grequests.get(page, headers=HEADERS) for page in region.links_list),
                position=0, leave=False,
                desc=f'Ищем информацию о школах в {reg}'):
            if knot.status_code != 200:
                bad_knots.append(knot.url)
            else:
                responses = [f'https://bus.gov.ru/public/agency/agency.json?agency={i["agencyId"]}' for i in
                             knot.json()['agencies']]
                for r in grequests.map(grequests.get(school, headers=HEADERS) for school in
                                       responses):
                    if r.status_code != 200:
                        bad_schools.append(r.url)
                    else:
                        base.append(School(r.json()['agency'], reg).info)

    print(f'Узлов не отвечает - {len(bad_knots)}')
    print(f'Школ не отвечает -  {len(bad_schools) - 1}')
    print(f'Добавлено в базу {len(base)} записей')

    with open('bad_schools.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(bad_schools))
        file.close()

    with open('bad_knots.txt', 'w', encoding='utf-8') as file:
        file.write('\n'.join(bad_knots))
        file.close()

    base = [row for row in base if row != []]

    with open('base.csv', 'w') as f:
        w = csv.writer(f)
        w.writerows(base)
        f.close()


if __name__ == '__main__':
    parsing()
    print('Готово!')

