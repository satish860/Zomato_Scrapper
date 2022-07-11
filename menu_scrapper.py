import json
from bs4 import BeautifulSoup
import extruct as ex
from selenium import webdriver
import time
import os


def get_menus(url):
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
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(
        executable_path=r"chromedriver.exe")  # this might need a change since i am working in pycharm you might need to import os

    # url of the website of particular cities you want to scrap.
    driver.get(url)

    time.sleep(2)  # Allow 2 seconds for the web page to (open depends on you)
# You can set your own pause time. dont slow too slow that might not able to load more data
    scroll_pause_time = 10
    screen_height = driver.execute_script(
        "return window.screen.height;")  # get the screen height of the web
    i = 1

    while True:
        # scroll one screen height each time
        driver.execute_script(
            "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script(
            "return document.body.scrollHeight;")
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    menus = []

    for item in soup.select('.sc-1s0saks-17'):
        menu = {}
        try:
            # print(item)
            menu["name"] = item.select_one(".sc-1s0saks-15").text
            menu["price"] = item.select_one(".sc-17hyc2s-1").text
            menu["image"] = item.select_one(".sc-s1isp7-5").get("src")
            menus.append(menu)

        except Exception as e:
            # raise e
            print(e)
    return menus


with open('Resturant_list.json') as f:
    data = json.load(f)
details = []
i = 3
count = 0
for resturant in data:
    if count == i:
        break
    else:
        print("Getting menu from " + resturant["name"])
        url = resturant["order_url"]
        base_url = f"https://www.zomato.com{url}"
        if not os.path.exists(resturant["name"]+"_menu.json"):
            count += 1
            json.dump(get_menus(base_url), open(
                resturant["name"]+"_menu.json", "w"))
            time.sleep(60)
