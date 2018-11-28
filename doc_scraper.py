"""
Extract from the API Settings doc useful information
https://www.algolia.com/doc/api-reference/settings-api-parameters/
"""

import requests
from bs4 import BeautifulSoup

res = requests.get("https://www.algolia.com/doc/api-reference/settings-api-parameters/")
content = BeautifulSoup(res.content, 'html.parser')

anchor_containers = content.find_all('h4')
tables = content.find_all(class_='table-parameters-list-small')

for i in range(len(tables)):
    trs = tables[i].find_all('tr')
    anchor_name = anchor_containers[i].get_text()
    print()
    print(anchor_name)

    for tr in trs:
        a = tr.find_all('td')[0].find('a')
        page = requests.get('https://www.algolia.com/' + a.get("href"))
        page_content = BeautifulSoup(page.content, 'html.parser')

        labels = page_content.find_all(class_='rest-table-param-type-label')
        type = labels[0].get_text()
        default = labels[1].find('code').get_text() if labels[1].find('code') else labels[1].get_text()

        print(a.get_text().strip() + ' | ' + str(type) + ' | default: ' + str(default))