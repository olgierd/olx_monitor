#!/usr/bin/python3

import bs4
import hashlib
import requests
import time

sleeptime = 30
url = "https://www.olx.pl/poznan/q-skuter-125/?search%5Bfilter_float_price%3Ato%5D=5000&search%5Bdist%5D=100"

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
        ad_url = ad.find('a')['href']
        out.append({"title": title, "qth": qth, "date": date, "price": price, "url": ad_url})

    return out


def notify(message):
    try:
        print(message)
        requests.get(f"https://api.telegram.org/{token}/sendMessage", params={'chat_id': chat_id, 'text': message})
        time.sleep(3)
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
        md5 = get_md5(ad['title']+ad['qth'])
        if md5 not in hashes and not initial_run:
            notify(f"New ad {ad['title']} {ad['qth']} {ad['price']} {ad['url']}")
        hashes.add(md5)

    print(f"Monitoring {len(hashes)} ads.")

    initial_run = False

    time.sleep(sleeptime)
