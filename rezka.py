import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

url = 'https://rezka.ag/films/best/'
urls = []
links_spis = []
FILM_INFO = []
film_info = []

for i in range(1, 4):
    urls.append(f'{url}page/{i}/')
for h in urls:
    r = requests.get(h, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    item_link = soup.find('div', class_ = 'b-content__inline_items')
    for i in item_link.findAll('div', class_ = 'b-content__inline_item-link'):
        ur = str(i.find('a').get('href'))
        links_spis.append(ur)
for i in links_spis:
    response = requests.get(i, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    item_name = soup.find('div', class_ = 'b-post__title')
    for k in item_name.findAll('h1'):
        global name
        name = k.text
    item_combo = soup.find('table', class_ = 'b-post__info')
    combo = []
    global actors
    actors = ''
    for k in item_combo.findAll('tr'):
        for h in k.findAll('td'):
            combo.append(h.text)
        for h in k.findAll('span', class_ = 'item'):
            for l in h.findAll('a'):
                for f in l.findAll('span'):
                    actors = actors+f.text+', '
    combo = combo[1::2]

    if len(combo)>10:
        film_info = [name, combo[4], combo[3], combo[10], combo[6], combo[5], actors, combo[9], i]
    FILM_INFO.append(film_info)
    for k in range(len(FILM_INFO)):
        srez = FILM_INFO[k]
        if srez == []:
            FILM_INFO.pop(k)
    film_info = []

index = []
for i in range(len(FILM_INFO)):
    index.append(f'#{i+1}')

df = pd.DataFrame(list(FILM_INFO),
                  index = index,
                  columns = ['Название', 'Страна', 'Выход','Длительность', 'Жанр', 'Режисер', 'Актеры', 'Возрасной рейтинг', 'Ссылка'])
df.to_excel('Top_film.xlsx')

