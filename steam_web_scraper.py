from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
import datetime
import csv
import os.path
import chime

def check_price():
    # cookies set to bypass Steam's age check
    cookies = {'birthtime': '568022401'}
    URL = 'https://store.steampowered.com/app/1245620/ELDEN_RING/'
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
    page = requests.get(URL, headers = headers, cookies = cookies)

    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

    title = soup2.find(id='appHubAppName').get_text()
    title = title.strip()

    price = soup2.find('div', {'class': 'game_purchase_price price'}).get_text()
    price = price.strip()[1:]

    today = datetime.date.today()

    header = ['Title', 'Price', 'Date']
    data = [title, price, today]

    path = './steam_web_scraper_dataset.csv'
    check_file = os.path.isfile(path)

    # appends data to the file or creates a new file if one does not exist
    if check_file == True:
        with open('steam_web_scraper_dataset.csv', 'a+', newline = '', encoding = 'UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(data)
    else:
        with open('steam_web_scraper_dataset.csv', 'w', newline = '', encoding = 'UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerow(data)

    df = pd.read_csv(r'/Users/codybarnes/Desktop/projects/python/steam_web_scraper_dataset.csv')
    print(df)

    # program makes a sound if the price is bellow 59.99
    if float(price) < 59.99:
        chime.theme('pokemon')
        chime.success()

# runs every 24 hours after being started
while(True):
    check_price()
    time.sleep(86400)