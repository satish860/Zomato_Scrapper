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
resturants = {}
for item in ldjson['json-ld']:
    if "ItemList" == item["@type"]:
        resturants["itemList"] = item["itemListElement"]
    if "ListItem" == item["@type"]:
        resturants["Item"] = item["item"]

InitialResturantArray = []

for toplevel in resturants["itemList"]:
    resturant = {
        "name": resturants["Item"][toplevel["position"]-1]["name"],
        "image": resturants["Item"][toplevel["position"]-1]["image"],
        "order_url": toplevel["url"]
    }
    InitialResturantArray.append(resturant)

json.dump(InitialResturantArray,open("Resturant_list.json", "w"))
