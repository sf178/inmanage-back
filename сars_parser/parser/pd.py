# -*- coding: utf-8 -*-
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

url = "https://auto.ru/cars/mercedes/c_klasse/all/?page="  # Replace with your desired URL
pages = 5
headers = '''
authority: auto.ru
method: GET
path: /cars/mercedes/c_klasse/all/
scheme: https
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
accept-encoding: gzip, deflate, br
accept-language: ru,en;q=0.9,de;q=0.8
cache-control: max-age=0
cookie: _ym_uid=1605556268270668975; mindboxDeviceUUID=91fd8634-2807-43b7-8531-e4b3da5f0baa; gradius=300; autoru_gdpr=1; suid=dd3e32a89fb2e83d4d01efb184118752.454e54f26d9d7025efcaead64b8f67bb; gdpr=0; yandex_login=dmitrynekrylov; L=QHJ+Z25Ne31ZWn9+TUBFWGZ0DmV4TgULL1QkABQ2HycqQwseFj4=.1666391594.15137.349875.2a693b77834a8dc9104543e8bb5ebeee; yandexuid=9314193631596819544; i=2FOTbcRBod+F+ow2NLWCTm1DnX+ZnwakZO0tfYhvrNxx9ySYXum1IJElWN5onWetkKBcOuqKkoXmT5Kt1Eqrglg0h/I=; autoru_sid=43985888%7C1685984109613.7776000._7fYtOUFN8YXkzl1FJesgQ.DjwTWzda5zuaFGYHAkSxg5Lb6PRvvyfWfgxVvhvnofo; autoruuid=g647e13652krtsp1ls9ampligs6kvhtb.6a48781228ded606e60fcee22e6834f9; yuidlt=1; crookie=ptOWAQU0V6oACT6bDo2yZ3mqXDoMeToGgEZR+gCilpd73zlG7oF4jQT/MGLoD9c0YT6Ae24T0hOcxmd5QwpwzqqueIc=; cmtchd=MTY4ODUwNTYxMjI2OA==; my=YysBMwA=; index-selector-tab=marks; _csrf_token=44420caa87f8371c3f967e3f08849f32d01ae0f3f2aa834b; from=direct; _yasc=Uw5CdAhrQoOjDSjXfPHZXF12cUjtl8QqkBLEavmNddX6CZesRr76ZHxE6d2/Mw==; layout-config={"screen_height":1080,"screen_width":1920,"win_width":1872,"win_height":950}; _ym_isad=2; Session_id=3:1688596096.5.1.1596819567882:YOdfAg:2b.1.2:1|203406871.0.2|652648384.69572027.2.1:124846631.2:69572027|61:10014449.245301.RrAeDqaQyCQChCVjrRF-ZcZacFw; sessar=1.107.CiB2EWGSZWUDGS51tqBz-juZuib1_EkD36uqaTAwQeNwkw.QN7ExlkaJIOdeWjBeKB5cAGVa6LDaUITVd5yXuT46Sc; ys=udn.cDrQlC4%3D#c_chck.2457308912; mda2_beacon=1688596096294; sso_status=sso.passport.yandex.ru:synchronized; yaPassportTryAutologin=1; _ym_d=1688596252; count-visits=3; from_lifetime=1688596257396; cycada=YfOczvUG3WjOxDheWDEYFBRih1gw8tqY7c1uaGWNrW0=
sec-ch-ua: "Chromium";v="112", "YaBrowser";v="23", "Not:A-Brand";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.4.674 Yowser/2.5 Safari/537.36
'''
headers_split = headers.strip().split('\n')
#print(headers_split)
headers_dict = {}
for header in headers_split:
    if header != '':
        #print(header)
        key, value = header.split(': ')
        headers_dict[key] = value

response = requests.get(url + str(1), headers=headers_dict)
response.encoding = "utf-8"

html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')

item = soup.find('script', class_='RIS').text

with open('data.txt', 'w', encoding="utf-8") as f:
    f.write(item)
    f.close()
#print(item)
# with open('data.json', 'w') as f:
#     json.dump(item, f)


# for page in range(1, pages + 1):
#     response = requests.get(url + str(page), headers=headers_dict)
#     html_content = response.text
#
#     #print(html_content)
#
#     soup = BeautifulSoup(html_content, 'html.parser')
#
#     item = soup.find('script', class_='RIS')
#     print(item.text.strip())
    # listing_items = soup.find_all('div', class_='ListingItem')
    # pr_list = []
    # for item in listing_items:
    #     #print(item)
    #     title_link = item.find('a', class_='Link ListingItemTitle__link')
    #     title = title_link.text.strip().replace('ÐÐ»Ð°ÑÑ', 'Class').replace('Ð ÐµÑÑÐ°Ð¹Ð»Ð¸Ð½Ð³', 'Restyle')
    #     href = title_link['href']
    #
    #     price_element = item.find('div', class_='ListingItemPriceNew__content-HAVf2')
    #     if price_element:
    #         # pr_list.append(price_element)
    #         price = price_element.text.strip().replace('Â ', ' ').replace('â½', 'rub')
    #     else:
    #         price = None
    #     # Finds the span element with class exactly matching "ListingItemPriceNew__content"
    #
    #     year = item.find('div', class_='ListingItem__year').text.strip()
    #
    #     km_age = item.find('div', class_='ListingItem__kmAge').text.strip().replace('Â ', ' ').replace('ÐºÐ¼', 'km').replace('ÐÐ¾Ð²ÑÐ¹', 'None')
    #     # print()
    #     # pr_list.append(km_age)
    #     #
    #     print('Title:', title)
    #     print('URL:', href)
    #     print('Price:', price)
    #     print('Year:', year)
    #     print('Kilometer Age:', km_age)
    #     print('---')
    # print(pr_list)