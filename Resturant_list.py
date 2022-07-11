import requests
from bs4 import BeautifulSoup
from pyld import jsonld
import json
import extruct as ex

url = "https://www.zomato.com/bangalore/delivery-in-brookefield"
# -*- coding: utf-8 -*-

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}


response = requests.get(url, headers=headers)


# soup = BeautifulSoup(response.text, 'html.parser')

ldjson = ex.extract(response.text, syntaxes=['json-ld'])
for item in ldjson['json-ld']:
    print("--------------------------")
    if "ListItem" == item["@type"] or "ItemList" == item["@type"]:
        print(item)

# for scripttag in soup.find_all('script',{'type':'application/ld+json'}):
#     print("-----------------------------------------")
#     expanded = jsonld.expand(scripttag.text)
#     print(json.dumps(expanded, indent=4))
