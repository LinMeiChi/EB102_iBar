# 簡易版
# 從 python 上傳到 elasticsearch，以kibana呈現

from elasticsearch import Elasticsearch
import csv
import datetime
import re
import requests


## 測試連線狀況(成功，會出現<Response [200]>)
# url = 'http://192.168.254.137:9200'
# connection_status =  requests.get(url)
# print(connection_status)

# 連到elasticsearch
es = Elasticsearch("http://192.168.254.137:9200")

# print(es)
csvfile = open('./whiskey_all-user.csv','r',encoding='utf-8',errors='ignore')
reader = csv.reader(csvfile)

for row in reader:
    if reader.line_num == 1: #去除第一列(欄位名稱)
        continue
    else:
        whiskey_name = row[0]
        user_name = row[1]
        text = row[2]
        language = row[3]
        score = row[4]
        timestamp = datetime.datetime.strptime(row[5],"%Y-%m-%d %H:%M:%S")
        abv = row[6]
        brand_country = row[7]
        official_content = row[8]
        whiskey_type = row[9]
        year = row[10]
        location = row[11]
        lat = float(re.sub(r'[\[\]]','',location).split(',')[1])
        lon = float(re.sub(r'[\[\]]','',location).split(',')[0])

        mappings =  {'whiskey_name':whiskey_name,'user_name':user_name,'text':text,'language':language,
                     'score':score,'timestamp':timestamp,'abv':abv,'brand_country':brand_country,
                     'official_content':official_content,'whiskey_type':whiskey_type,'year':year,'location':{'lat':lat,'lon':lon}}
        # print(mappings)

        # index可以從kibana介面建立，也可以使用下面程式碼建立
        # es.indices.create(index='index名稱', body=上面整理好的body)
        res = es.index(index='whiskey_kibana_final',doc_type='_doc',body=mappings)  # 已使用介面建立，故無需再使用程式建立
        print(res['result'])





        # # get: 回傳index信息
        # index_result = es.indices.get(index='whiskey_kibana_final') #index指定要get哪個index的資訊
        # print(index_result)
        #
        # # exists:查看index是否存在，回傳True/False
        # result = es.indices.exists(index='whiskey_kibana_final')
        # print(result)