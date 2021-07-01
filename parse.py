from os import write
from bs4 import BeautifulSoup
import requests
import csv

CSV = "items.csv"
HOST = "https://www.avito.ru/"
URL = "https://www.avito.ru/sankt-peterburg/telefony/mobile-ASgBAgICAUSwwQ2I_Dc?cd=1&p=1"
HEADERS = {
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.216 YaBrowser/21.5.4.610 Yowser/2.5 Safari/537.36"
}

def get_htmlcode(url, params=""):
    response = requests.get(url, headers=HEADERS, params=params)
    return response

def get_content(html):
    dat = BeautifulSoup(html, 'html.parser')
    items = dat.find_all('div', class_ = 'iva-item-content-m2FiN')
    phones =[]

    for item in items:
        phones.append(
            {
                'title':item.find('div', class_= 'iva-item-titleStep-2bjuh').get_text(strip = 'true'),
                'link':HOST + item.find('div', class_='iva-item-titleStep-2bjuh').find('a').get('href'),
                'price':item.find('div', class_ = 'iva-item-priceStep-2qRpg').find('span').get_text(strip = 'true')
            }
        )
    return phones

def put_in_file(items, path):
    with open(path, 'w',newline='') as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow(['Название модели', 'Ссылка на телефон', 'Цена'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price']])
def parse():
    RAW = input("Введите количество страниц:")
    RAW = int()
    html = get_htmlcode(URL)
    print(get_content(get_htmlcode(URL).text))
    if html.status_code == 200:
        phones =[]
        for p in range(1, RAW + 1):
            print('обработка страницы №', p)
            html = get_htmlcode(URL, params = {'p':p})
            phones.extend(get_content(html.text))
            put_in_file(phones, CSV)
            pass
    else:
        print("Error")
parse()