import requests
from bs4 import BeautifulSoup
url = "https://www.zomato.com/bangalore/delivery-in-brookefield"
# -*- coding: utf-8 -*-

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}


response = requests.get(url, headers=headers)


soup = BeautifulSoup(response.text, 'html.parser')

for scripttag in soup.find_all('script',{'type':'application/ld+json'}):
    print("-----------------------------------------")
    print(scripttag.text)