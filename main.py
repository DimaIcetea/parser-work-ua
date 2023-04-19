import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cards.csv'
HOST = 'https://www.work.ua'
URL = 'https://www.work.ua/jobs-python/'
HEADERS = {
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='card card-hover card-visited wordwrap job-link')
    cards = []

    for item in items:
        cards.append(
            {
            'title':item.find('h2').find('a').get_text(),
            'link_product':HOST + item.find('h2').find('a').get('href'),
            'brand':item.find('div', class_='add-top-xs').find('b').get_text(),
            }
        )
    return cards

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название работы', 'Ссылка на обьявление', 'Компания'])
        for item in items:
            writer.writerow([item['title'], item['link_product'], item['brand']])

def parser():
    PAGENATION = input("Укажите кол-во страниц для парсинга: ")
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION + 1):
            print(f'Парсим страницу: {page}')
            html = get_html(URL, params={'page': page})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV)
        else:
            print('Error')

parser()