# 使用textblob做情感分析
import re
import googletrans
from textblob import TextBlob
from pymongo import MongoClient
from openpyxl import load_workbook
import emoji
import pandas as pd
import csv

# --------------- 將非英文的評論做翻譯 ---------------
def trans(text):
    # Initial
    translator = googletrans.Translator()
    # Basic Translate
    results = translator.translate(text).text
    print(results)
    # print("--------------")
    return results

# --------------- 將表情符號轉換成文字 ---------------
def emoji_text(tran):
    em_text = emoji.demojize(tran)
    # print(em_text)

    return em_text

# --------------- 去除非必要字元 ---------------
def get_tokens(emo):
    subtext = re.sub(r'★','',emo)
    # print(subtext)
    # print("--------------")
    return subtext

# ---------------------------------------------------    利用textblob做情感分析  --------------------------------------
def get_TextBlob(gt_texts):
    blob = TextBlob(gt_texts).sentences
    # all_blob = blob.sentiment
#     data['Polarity'] = all_blob[0]
#     # print('polarity:', all_blob[0])
#     data['Subjectivity'] = all_blob[1]
#     # print('subjectivity:', all_blob[1])
#     if data['Polarity'] < 0:
#         data['Analysis'] = 'Negative'
#     elif data['Polarity'] > 0:
#         data['Analysis'] = 'Positive'
#     else:
#         data['Analysis'] = 'Neutral'
#     print("把一段文本分成了不同的句子    ",blob)
#     print("--------------------")

# --------------- 主程式 ---------------
def main(text):
    tran = trans(text)
    emo = emoji_text(tran)
    non_essential = get_tokens(emo)
    get_TextBlob(non_essential)

# --------------- 取資料 ---------------
if __name__ == "__main__":

    ##　取xlsx
    wb = load_workbook('./try_csv/all_user_subnull_trans.xlsx')
    sheet = wb.active
    for row in sheet.rows:
        # 酒名
        name = row[0].value
        if name == '酒名':
            continue
        else:
            whiskey_name = name
            # 使用者名稱
            user_name = row[1].value
            all_text = str(row[2].value)


    ## 取csv檔
    # csvfile = open('./try_csv/whiskey_all-user.csv', 'r', encoding='utf-8',errors='ignore')
    # # csvfile = open('./finalV2.csv', 'r',encoding='utf-9',errors='ignore')
    # reader = csv.reader(csvfile)
    # for row in reader:
    #     if reader.line_num == 1:  # 去除第一列(欄位名稱)
    #         continue  # skip first row
    #     else:
    #         whiskey_name = row[0]
    #         user_name = row[1]
    #         score = row[2]
    #         all_text = row[3]


    ## 從 mongo 取
    # uri = f'mongodb://user_name:password@localhost/'
    # client = MongoClient(uri)  # 連線本地MongoDB資料庫
    # db = client.Whiskey  # DB名
    # collections = db.Whiskey  # 桶子名
    # for item in collections.find():
    #     # print(item)
    #     whiskey_name = item['whiskey_name']
    #     # data['whiskey_name'] = whiskey_name
    #     # print(whiskey_name)
    #     comment = item['comment']
    #     # print(comment)
    #     for un in comment:
    #         user_name = un['user_name']
    #         # data['user_name'] = user_name
    #         score = un['score']
    #         # data['score'] = score
    #         all_text = un['text']
    #         print(all_text)
        if all_text == 'null' or all_text == '':
            continue
        else:
            text = all_text
            print(text)
            main(text)
