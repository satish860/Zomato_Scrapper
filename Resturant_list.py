import json
import extruct as ex
from selenium import webdriver
import time


url = "https://www.zomato.com/bangalore/delivery-in-brookefield"
# -*- coding: utf-8 -*-

headers = {
    'authority': 'scrapeme.live',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

driver = webdriver.Chrome(
    executable_path=r"chromedriver.exe")  # this might need a change since i am working in pycharm you might need to import os

driver.get(url)  # url of the website of particular cities you want to scrap.

time.sleep(2)  # Allow 2 seconds for the web page to (open depends on you)
scroll_pause_time = 3  # You can set your own pause time. dont slow too slow that might not able to load more data
screen_height = driver.execute_script("return window.screen.height;")  # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break


# soup = BeautifulSoup(response.text, 'html.parser')

ldjson = ex.extract(driver.page_source, syntaxes=['json-ld'])
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
