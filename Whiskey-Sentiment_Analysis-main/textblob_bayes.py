# 利用textblob情感分析後的結果，做樸素貝葉斯分類演算法
import csv
from math import floor
from sklearn.model_selection import train_test_split
from textblob.classifiers import NaiveBayesClassifier

#Train
csvfile_train = open('./try_csv/70_each_textblob.csv', 'r',encoding='utf-8',errors='ignore')  #errors='ignore'
readers = csv.reader(csvfile_train)
train = []
for row_train in readers:
    x = ()
    if readers.line_num == 1:  # 去除第一列(欄位名稱)
        continue  # skip first row
    else:
        text = row_train[1]
        analysis = row_train[4]
        if analysis == 'Positive' or row_train[4] == 'Neutral':
            analysis = 'pos'
        else:
            analysis = 'neg'
        x += text,analysis
        train.append(x)
# print(train)

# Test
csvfile_test = open('./try_csv/30_each_textblob.csv', 'r',encoding='utf-8',errors='ignore')  #errors='ignore'
read = csv.reader(csvfile_test)
test = []
for row_test in read:
    y = ()
    if read.line_num == 1:  # 去除第一列(欄位名稱)
        continue  # skip first row
    else:
        text_t = row_test[1]
        analysis = row_test[4]
        if analysis == 'Positive' or row_test[4] == 'Neutral':
            analysis = 'pos'
        else:
            analysis = 'neg'
        y += text_t,analysis
        test.append(y)
# print(test)
#
# 把訓練丟進去訓練
nb_model = NaiveBayesClassifier(train)
#
# 預測新來的樣本
dev_sen = "Very good, suprinsgly, remind me of the 10."
print(nb_model.classify(dev_sen))
# 計算屬於某一類的概率
dev_sen_prob = nb_model.prob_classify(dev_sen)
print("屬於pos的機率 ",dev_sen_prob.prob("pos"))
print("屬於neg的機率 ",dev_sen_prob.prob("neg"))
print("--------------------")
# 計算測試集的精確度
print('test的精確度',nb_model.accuracy(test))






