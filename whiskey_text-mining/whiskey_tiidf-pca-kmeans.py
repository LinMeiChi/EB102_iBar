import pandas as pd

# ----- 讀取檔案 -----
df = pd.read_csv(r'./whiskey_tfidf.csv', encoding='utf-8')
# 法一:
# csvfile1 = df.loc[:, ~df.columns.str.match('Unnamed')]

# 法二:
# 透過 drop() 方法來刪除觀測值或欄位，指定參數 axis = 0 表示要刪除觀測值（row），指定參數 axis = 1 表示要刪除欄位（column）。
csvfile = df.drop(['Unnamed: 0'], axis=1)

# ----- 標準化 -----
# PCA降維前，先標準化的好處:防止過分捕捉某些數值大的特徵、利於梯度下降法的收斂。 (https://www.zhihu.com/question/40956812)
# 正規化、標準化詳細介紹 (https://aifreeblog.herokuapp.com/posts/54/data_science_203/)
from sklearn import preprocessing
def Standardization(csvfile):
    tfidf_scale = preprocessing.scale(csvfile, axis=0, with_mean=True, with_std=True, copy=True)
    # print(tfidf_scale)
    # print('原始维度: ', len(tfidf_scale[0]))
    return tfidf_scale

# ----- PCA 降維 -----
# 通過降維的方式對資料進行壓縮，從而加快我們的學習速率。
# PCA、K-means 詳細介紹 (https://www.itread01.com/content/1546355190.html)
from sklearn.decomposition import PCA
def PCA_DimensionReduction(tfidf_stand,dimension):
    pca = PCA(n_components=dimension)    # 初始化PCA降維後的維度
    X_pca = pca.fit_transform(tfidf_stand)   #　進行降維
    # print(X_pca)
    return  X_pca

# ----- K-means 聚類演算法 -----
# K-Means 演算法可以非常快速地完成分群任務，但是如果觀測值具有雜訊（Noise）或者極端值，其分群結果容易被這些雜訊與極端值影響，適合處理分布集中的大型樣本資料。 ( https://ithelp.ithome.com.tw/articles/10187314 )
# 是非監督式學習，「物以類聚」概念。 (https://medium.com/@chih.sheng.huang821/%E6%A9%9F%E5%99%A8%E5%AD%B8%E7%BF%92-%E9%9B%86%E7%BE%A4%E5%88%86%E6%9E%90-k-means-clustering-e608a7fe1b43)
# 各項參數說明 ( https://www.itread01.com/content/1550612527.html )
from sklearn.cluster import KMeans
def kmeans(PCA_DR, k):
    clusterer = KMeans(n_clusters=k,init='k-means++')    # 設置聚類模型
    k_fit = clusterer.fit(PCA_DR)   # .fit()訓練模型
    labels = k_fit.labels_  # labels為分類的標籤
    # y = clusterer.fit_predict(PCA_DR)  # .fit_predict()訓練模型並執行聚類，返回每個樣本所屬的簇標記

    # kmeans聚類結果
    labels_cluster_frame = pd.DataFrame(labels, columns=['labels_cluster'])
    # print(labels_cluster)

    # PCA 降維結果
    pca_frame = pd.DataFrame(PCA_DR, columns=['x1', 'x2', 'x3'])
    # print(pca_frame)

    # 將 PCA 和聚類併接 ( https://blog.csdn.net/chixujohnny/article/details/68059992 )
    # axis=1: 列併接。
    PCA__cluster_frame = pd.concat([pca_frame, labels_cluster_frame], axis=1 )
    print('--------------- 分',k,'群，聚類結果: ---------------')
    print(PCA__cluster_frame)
    # 儲存PCA和聚類結果
    # PCA__cluster_frame.to_csv(r'./whiskey_tfidf_pca_k-meaans.csv', encoding='utf-8-sig')
    # print(clusterer.inertia_)
    return labels

# # ----- BIRCH 聚類演算法 -----
# from sklearn.cluster import Birch
# def birch(PCA_DR, k):
#     clusterer = Birch(n_clusters=k)
#     y = clusterer.fit_predict(PCA_DR)
#     print('分',k,'群，聚類結果:')
#     print(y)

if __name__ == '__main__':
    tfidf_stand = Standardization(csvfile)
    PCA_DR = PCA_DimensionReduction(tfidf_stand, dimension=3)
    # k = 7   # 分7群
    for k in range(3,11):
        kmeans_y = kmeans(PCA_DR, k)
        # b_y = birch(PCA_DR, k)

