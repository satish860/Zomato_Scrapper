import json
import extruct as ex
import requests


def resturant_details(url):
    base_url = f"https://www.zomato.com{url}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    response = requests.get(base_url, headers=headers)
    ldjson = ex.extract(response.text, syntaxes=['json-ld'])
    resturants = {}
    for item in ldjson['json-ld']:
        if("Restaurant" == item["@type"]):
            resturants["name"] = item["name"]
            resturants["openingHours"] = item["openingHours"]
            resturants["address"] = item["address"]
            resturants["image"] = item["image"]
            resturants["servesCuisine"] = item["servesCuisine"]
            resturants["telephone"] = item["telephone"]
            resturants["address"] = item["address"]
    return resturants


with open('Resturant_list.json') as f:
    data = json.load(f)
details = []
for resturant in data:
    details.append(resturant_details(resturant["order_url"]))

json.dump(details,open("Resturant_details.json", "w"))
