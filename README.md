# Whiskey-Sentiment_Analysis                                                                                                                                                       
textblob.py 👉 情感分析                                                                                                                                                             
textblob_bayes.py 👉 利用情感分析後的結果，作為樸素貝葉斯分類演算法的Train和Test資料集。可用來預測新評論的極性。                                                                           
nltk_bayes.py 👉 利用NLTK的電影評論語料庫，作為樸素貝葉斯分類演算法的Train和Test資料集。可用來預測新評論的極性。                                                                           
# whiskey_ETL                                                                                                                                                                       
Whisky_Advocate.py 👉 whiskyadvocate網站爬蟲，使用一般的requests。
whisky_.influenster-selenium.py 👉 whiskyadvocate網站爬蟲，因為加密問題，無法爬取，故使用selenium。                                                                                   
# whiskey_text-mining
whiskey_tfidf.py 👉 先進行斷詞斷字、去除停用詞、詞性還原、詞性標註...等一系列動作，再對處理過的資料做tf-idf統計，來分析單詞的頻率。