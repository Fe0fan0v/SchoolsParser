import grequests
import json
from pprint import pprint

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
           '81.0.4044.138 YaBrowser/20.4.3.268 (beta) Yowser/2.5 Safari/537.36',
           'Accept': 'application/json, text/javascript, */*; q=0.01'}
with open('regions.json', 'r', encoding='utf-8') as fh:
    DATA = json.load(fh)


class Region:
    def __init__(self, name, page_size=30):
        self.page_size = page_size
        self.name = name
        self.quantity = DATA[name][1]
        self.links_list = [f'https://bus.gov.ru/public-rest/api/agency/search/init?d-442831-p={k}&'
                      f'orderAttributeName=rank&regionId={DATA[self.name][0]}&regions={DATA[self.name][0]}'
                      f'&orderDirectionASC=false&pageSize={self.page_size}&searchString=%D1%88%D0%BA%D0%BE%D0%BB%D0%B0'
                      f'&searchTermCondition=or'
                      for k in range(1, self.quantity // self.page_size + 2)]

    def get_links(self):
        jsons = grequests.map(grequests.get(page_url, headers=HEADERS) for page_url in self.links_list)
        jsons = list(filter(lambda x: x.status_code == 200, jsons))
        result = [[j['agencyId'] for j in [i for i in json_.json()['agencies']]] for json_ in jsons]
        schools = []
        for i in result:
            schools += i
        return [f'https://bus.gov.ru/public/agency/agency.json?agency={school_id}'
                for school_id in schools]

    def __str__(self):
        return self.name


class School:
    def __init__(self, school_json, region):
        self.link = f'https://bus.gov.ru/public/agency/agency.json?agency={school_json["id"]}'
        self.name = f'Проблема с названием в {self.link}' if None else school_json['shortClientName']
        self.address = f'Проблема с адресом в {self.link}' if None else school_json['agencyAddress']['fullAddress']
        try:
            self.oktmo_name = school_json['oktmo']['name']
            if self.oktmo_name.split()[0].startswith('п'):
                self.loc_type = 'Посёлок'
            elif self.oktmo_name.split()[0].startswith('д'):
                self.loc_type = 'Деревня'
            elif self.oktmo_name.split()[0].startswith('ст'):
                self.loc_type = 'Станица'
            elif self.oktmo_name.split()[0].startswith('с') and '-' not in self.oktmo_name.split()[0]:
                self.loc_type = 'Село'
            elif self.oktmo_name.split()[0].startswith('х'):
                self.loc_type = 'Хутор'
            elif self.oktmo_name.split()[0].startswith('аул'):
                self.loc_type = 'Аул'
            elif self.oktmo_name.split()[0].startswith('г'):
                self.loc_type = 'Город'
            elif self.oktmo_name.split()[0].startswith('Сел'):
                self.loc_type = 'Сельское поселение'
            elif self.oktmo_name.split()[0].startswith('р'):
                self.loc_type = 'Рабочий посёлок'
            elif len(self.oktmo_name.split()) > 1 and self.oktmo_name.split()[1].startswith('сель'):
                self.loc_type = 'Сельсовет'
            elif len(self.oktmo_name.split()) > 1 and self.oktmo_name.split()[1].startswith('мун'):
                self.loc_type = 'Муниципальный район'
            elif self.oktmo_name.startswith('Нас'):
                self.loc_type = 'Населённый пункт'
            elif self.oktmo_name.split()[0].startswith('у'):
                self.loc_type = 'Улус'
            elif self.oktmo_name.split()[0].startswith('ж'):
                self.loc_type = 'Железнодорожная станция'
            else:
                self.loc_type = 'Статус неизвестен'
        except:
            self.loc_type = 'Статус неизвестен'
        self.phone = f'Проблема с телефоном в {self.link}' if None else school_json['phone']
        self.site = f'Сайт не указан в {self.link}' if None else school_json['website']
        self.director = f'Проблема с директором в {self.link}' if None else f"{school_json['managerSecondName']} " \
                        f"{school_json['managerFirstName']} "  \
                        f"{school_json['managerMiddleName']}"
        self.email = f'Не указан Email в {self.link}' if None else f"{school_json['email']}"
        self.region = region
        self.info = [self.name, self.director, self.address, self.loc_type, self.region, self.phone, self.site,
                     self.email, self.link]

    def __str__(self):
        return self.name
