
import requests
from lxml import html
import json
import csv


def check_status(username, password):
    url = 'http://45.55.213.78/login'

    h = {'Accept': 'application/json, text/plain, */*',
         'Content-Type': 'application/json',
         'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36', }

    d = {"useremail": username, "userpassword": password}
    req = requests.session()
    response = req.post
    response = req.post(url, data=json.dumps(d), headers=h)

    final_page = req.get('http://45.55.213.78/getwebsitedata')
    data = final_page.text
    data.strip('/n')
    data = ''.join(data.split())
    data = json.loads(data)
    data = data.get('data')
    error_sites = []
    site = []

    for i in data:
        name = i['site_url']
        for j in i['sub_url_details']:
            site_path = j['site_url']
            for k in j['xpaths']:
                if k['status'] == False:
                    site.append(
                        {'name': name, 'site_link': site_path, 'xpath': k['xpath'], 'field': k['name']})

    print(site)
