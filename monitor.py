#!/usr/bin/python3

import bs4
import hashlib
import requests
import time

cena = 5000
dystans = 100
sleeptime = 30

url = f"https://www.olx.pl/poznan/q-skuter-125/?search%5Bfilter_float_price%3Ato%5D={cena}&search%5Bdist%5D={dystans}"

###########################################################################

with open('secrets.txt') as secrets:
    token, chat_id = secrets.read().splitlines()


def get_ads():
    page = requests.get(url).content
    parser = bs4.BeautifulSoup(page, "html.parser")

    ads = parser.find("table", {"class": "fixed offers breakword redesigned"}).find_all('table')

    out = []

    for ad in ads:
        title, price = [x.text for x in ad.find_all("strong")]
        qth, date = [x.next for x in ad.find_all("i")]
        out.append({"title": title, "qth": qth, "date": date})

    return out


def notify(message):
    try:
        print(message)
        requests.get(f"https://api.telegram.org/{token}/sendMessage", params={'chat_id': chat_id, 'text': message})
    except Exception:
        print(">>> Sending notification failed.", message)


def get_md5(title):
    h = hashlib.new('md5')
    h.update(title.encode())
    return h.hexdigest()


hashes = set()
initial_run = True

while True:
    for ad in get_ads():
        md5 = get_md5(ad['title'])
        if md5 not in hashes and not initial_run:
            notify(f"New ad {ad['title']} {ad['qth']} {ad['price']} {ad['date']}")
        hashes.add(md5)

    print(f"Monitoring {len(hashes)} ads.")

    initial_run = False

    time.sleep(sleeptime)