import requests
from bs4 import BeautifulSoup
import os
import  pandas


file_data = (r'./liqueur')
if not os.path.exists(file_data):
    os.mkdir(file_data)

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
           "referer": "https://www.whiskyadvocate.com/ratings-reviews/?search=&submit=&brand_id=0&rating=0&price=0&category=0&styles_id=0&issue_id=0"}
url = 'https://www.whiskyadvocate.com/ratings-reviews/?search=&submit=&brand_id={}&rating=0&price=0&category=0&styles_id=0&issue_id=0'
ss=requests.session()
res = ss.get(url, headers=headers)

soup = BeautifulSoup(res.text, "html.parser")

brand_totle = soup.select('option')

for brand_Web in brand_totle:
    if brand_Web['value'] == '316':
        continue
    else:
        brand_value = brand_Web['value']
        url_a = 'https://www.whiskyadvocate.com/ratings-reviews/?search=&submit=&brand_id={}&rating=0&price=0&category=0&styles_id=0&issue_id=0'
        ss = requests.session()
        url_b = url_a.format(brand_value)
        res = ss.get(url_b, headers=headers)

        soup = BeautifulSoup(res.text, "html.parser")

        Web = [url_a.format(brand_value)]
        for net in  Web:
            # print(net)
            brand = soup.select('h1[itemprop="name"]')      #定位酒名+濃度
            if brand == []:
                continue
            else:
                print(brand)
                for brand_a in brand:
                    brand_name = brand_a.text.split(',')[0]     #酒名
                    print(brand_name)
                    abv = brand_a.text.split(',')[1]            #濃度
                    print(abv)

                    # brand_name = brand_a.text.split(',')[0]
                print("-----------------------")

