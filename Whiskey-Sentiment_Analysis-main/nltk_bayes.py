# 利用nltk做樸素貝葉斯分類演算法 (可參考 https://medium.com/@joel_34096/sentiment-analysis-of-movie-reviews-in-nltk-python-4af4b76a6f3）
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
import csv
import pandas as pd
csvfile = open('./try_csv/commit-comment.csv', 'r',encoding='utf-8',errors='ignore')
reader = csv.reader(csvfile)

#存
df = pd.DataFrame(columns=['酒名','評論','預測情緒','可能性'])
data = {"name": "","comment":"","prediction":"","possibility":""}
cocktail_list = []


# 情感分析是指確定一段给定的文本是積極還是消極的過程。

# 定義一個用於提取特徵的函數
# 輸入一段文本返回：{'It': True, 'movie': True, 'amazing': True, 'is': True, 'an': True}
# 返回類型是一个dict
def extract_features(word_list):
    return dict([(word, True) for word in word_list])

if __name__ == '__main__':
    # 加載積極與消極評論 ( 利用電影評論的語料庫)
    positive_fileids = movie_reviews.fileids('pos')
    negative_fileids = movie_reviews.fileids('neg')
    # print(type(positive_fileids), len(negative_fileids))

    # 將這些評論數據分成積極評論與消極評論
    # 結果為一個list
    features_positive = [(extract_features(movie_reviews.words(fileids=[f])), 'Positive') for f in positive_fileids]
    features_negative = [(extract_features(movie_reviews.words(fileids=[f])), 'Negative') for f in negative_fileids]

    # 分成訓練數據集（80%）和測試數據集（20%）
    threshold_factor = 0.8
    threshold_positive = int(threshold_factor * len(features_positive))  # 800(因為len(positive_fileids)為1000,故1000*0.8=800)
    threshold_negative = int(threshold_factor * len(features_negative))  # 800
    # 提取特徵 800個積極文本和800個消極文本構成訓練集  200+200構成測試文本(1000-800=200)
    features_train = features_positive[:threshold_positive] + features_negative[:threshold_negative]
    features_test = features_positive[threshold_positive:] + features_negative[threshold_negative:]
    print("\n訓練資料量:", len(features_train))
    print("測試資料量:", len(features_test))

    # 訓練朴素貝葉斯分類器
    classifier = NaiveBayesClassifier.train(features_train)
    print("\n分類器的準確率:", nltk.classify.util.accuracy(classifier, features_test))

    print("\n十大出現較高的詞:")
    for item in classifier.most_informative_features()[:10]:
        print(item[0])

    # 輸入一些簡單的評論
    for row in reader:
        if reader.line_num == 1:  # 去除第一列(欄位名稱)
            continue  # skip first row
        else:
            name = row[0]
            data['name'] = name
            print("酒名: ", name)
            review = row[1]
            data['comment'] = review
            print("評論: ",review)
            # 運行分類器，獲得預測結果
            print("\n進行預測:")

            probdist = classifier.prob_classify(extract_features(review.split()))
            pred_sentiment = probdist.max()
            # 輸出
            data['prediction'] = pred_sentiment
            print("預測情緒:", pred_sentiment)
            possibility = round(probdist.prob(pred_sentiment), 2)
            data['possibility'] = possibility
            print("可能性:", round(probdist.prob(pred_sentiment), 2))
            print("----------------------------")
        cocktail_list.append(list(data.values()))
    # print(cocktail_list)
# dff = df.append(pd.DataFrame(cocktail_list, columns=['酒名','評論','預測情緒','可能性']))
# dff.to_csv(r'./try_csv/nltk-bayes_commit-comment.csv', index=False, encoding="utf-8-sig")