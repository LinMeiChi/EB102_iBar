# ===== 對內容進行 tf-idf
# ===== 英文內容有兩種方式:nltk、spacy(https://kknews.cc/zh-tw/code/34y9oka.html)
# ===== 使用 nltk

# ---------- 開啟檔案 ----------
import json
# 開啟txt檔
# with open("./c1.txt",'r') as load_f:
#     data = json.load(load_f)
#     for d in range(len(data)):
#         row_sentence = data[d]['details']['text'].replace('null','')
#         # print(row_sentence)
#         if row_sentence == '' or row_sentence == []:
#             pass
#         else:
#             texts.append(row_sentence)
#     # print(texts)

## 開啟csv檔
import csv
csvfile = open('./whiskey_comment_commit.csv', 'r', encoding='utf-8',errors='ignore')
# csvfile = open('./finalV2.csv', 'r',encoding='utf-9',errors='ignore')
reader = csv.reader(csvfile)

# ---------- 移除數字及特殊符號 ----------
import re
def get_tokens(text):  # 分詞函數，所有英語字母轉化為小寫方便在下一步進行分析，把數字刪除
    # print(text)
    remove_char = '[0-9’!"#$%&()*+-./:;<=>?@，。?★、…【】\'\r《》？“”‘’！\\\\[\\]^_`{|}~]+'
    lowers = re.sub(remove_char, '' , text).lower()
    # print("lowers=",lowers)
    return  lowers

# ---------- 使用nltk進行斷字斷詞 ----------
import nltk
def tokenize(remove_text):
    tokens = nltk.word_tokenize(remove_text)
    # print(tokens)
    return tokens

# ---------- 去除停用詞 ----------
from nltk.corpus import stopwords
def stop_words(tokens):
    filtered = [w for w in tokens if w not in stopwords.words('english')]
    # print(filtered)
    return filtered

# ---------- 詞性還原 ----------
from nltk.stem import WordNetLemmatizer
def lemmatize(stop_text):
    lemmas_sent = []
    for t_s in stop_text:
        wnl = WordNetLemmatizer()
        lemmatizer = wnl.lemmatize(t_s)
        lemmas_sent.append(lemmatizer)
    print(lemmas_sent)
    return lemmas_sent

# ---------- 詞性標註 ----------
from nltk.corpus import wordnet
def tag(tokens):
    tagged_sent = nltk.pos_tag(tokens)
    # print(tagged_sent)

    tags_set = []
    tag_text = []
    for tag_t in tagged_sent:
        # 只保留形容詞、名詞、感嘆詞
        if tag_t[1].startswith('J') or tag_t[1].startswith('N') or tag_t[1].startswith('UH'):
            tags_set.append(tag_t[1])
            tag_set = set(tags_set)

            if tag_t[1] not in tag_set:
                continue
            else:
                tag_text.append(tag_t[0])
    # print(tag_text)
    return tag_text

# ---------- 計算單字出現次數 ----------
from collections import Counter
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
def char_count(all_text,tag_text):
    each_text = " ".join(tag_text)
    all_text.append(each_text)
    # vectorizer = CountVectorizer(stop_words=None, token_pattern="(?u)\\b\\w\\w+\\b")
    # X = vectorizer.fit_transform(all_text)
    # r = pd.DataFrame(X.toarray(),columns=vectorizer.get_feature_names())
    # print(r)
    # print("-----------------------")
    return all_text

# ---------- 計算TF-IDF權重 ----------
'''
在scikit-learn中，有兩種方法進行TF-IDF的預處理。
方法一:CountVectorizer會計算單字出現在文件的次數；再透過TfidfTransformer轉換成TFIDF和IDF。
方法二:直接使用TfidfVectorizer計算TFIDF。
'''
from sklearn.feature_extraction.text import TfidfTransformer
# 方法一:
def tf_idf(whiskey_name_list,count_all_text):
    vectorizer = CountVectorizer(stop_words=None, token_pattern="(?u)\\b\\w\\w+\\b")
    X = vectorizer.fit_transform(count_all_text)
    transformer = TfidfTransformer(smooth_idf=True)
    tfidf_matrix = transformer.fit_transform(X)    #輸出的各個文字各個詞的TF-IDF值
    w = tfidf_matrix.toarray()
    tfidf = pd.DataFrame(w, columns=vectorizer.get_feature_names(),index=whiskey_name_list)  
    print(tfidf)
    print("------------------------------")

# from sklearn.feature_extraction.text import TfidfVectorizer
# # 方法二:
# def tf_idf(whiskey_name_list,count_all_text):
#     vectorizer = TfidfVectorizer(sublinear_tf=False, stop_words=None, token_pattern="(?u)\\b\\w+\\b", smooth_idf=True)
#     X = vectorizer.fit_transform(count_all_text)
#     w = X .toarray()
#     tfidf = pd.DataFrame(w, columns=vectorizer.get_feature_names(), index=whiskey_name_list)
#     print(tfidf)
#     print("------------------------------")

if __name__ == "__main__":
    all_text = []
    whiskey_name_list = []
    for row in reader:
        if reader.line_num == 1:  # 去除第一列(欄位名稱)
            continue  # skip first row
        else:
            whiskey_name = row[1]
            whiskey_name_list.append(whiskey_name)
            text = row[2]
            remove_text = get_tokens(text)
            tokenize_text = tokenize(remove_text)
            stop_words_text = stop_words(tokenize_text)
            lemmatize_text = lemmatize(stop_words_text)
            tags_text = tag(lemmatize_text)
            count_all_text = char_count(all_text,tags_text)
            tf_idf(whiskey_name_list,count_all_text)
