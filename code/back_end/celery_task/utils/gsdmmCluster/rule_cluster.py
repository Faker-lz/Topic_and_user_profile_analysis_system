import re
import pymongo
import pandas as pd
from collections import Counter
import math
from normalization import  normalize_corpus
from mgp import MovieGroupProcess
from tfidf import getKeywords_tfidf

import bson  #此处添加
mgp=MovieGroupProcess(K=6,alpha=0.01,beta=0.02,n_iters=40)


def compute_V(texts, V):
    for text in texts:
        for word in text:
            V.add(word)
    return len(V), V


def get_cluster_data(twitter_data, num_clusters):
    cluster_details = {}
    # 获取蔟的中心

    # 获取每个簇的关键特征
    # 获取每个簇的id
    for cluster_num in range(num_clusters):
        cluster_details[cluster_num] = {}
        cluster_details[cluster_num]['cluster_num'] = cluster_num  # 簇序号

        id_s = twitter_data[twitter_data['cluster'] == cluster_num]['_id'].values.tolist()
        cluster_details[cluster_num]['_id'] = id_s

        fulltext = twitter_data[twitter_data['cluster'] == cluster_num]['cleaned_fulltext'].values.tolist()
        cluster_details[cluster_num]['Cleaned_fulltext'] = fulltext

        scores = twitter_data[twitter_data['cluster'] == cluster_num]['score'].values.tolist()
        cluster_details[cluster_num]['scores'] = scores

    return cluster_details


def print_cluster_data(cluster_data):
    # print cluster details
    for cluster_num, cluster_details in cluster_data.items():
        print('Cluster{} details'.format(cluster_num))
        print('-' * 20)
        #         print('Key features:',cluster_details['key_features'])
        print('sentence in this clusters:')
        print('》'.join(cluster_details['Cleaned_fulltext'][:5]).replace('\n', ''))
        print('=' * 40)

client = pymongo.MongoClient('10.245.142.249', 27017)
# 连接所需数据库、集合,twitter_search为数据库名，task_post为表名
mongo_collection = client['twitter_search']['task_post']  # 28045条数据
result_cursor = mongo_collection.find_raw_batches(batch_size=1000)
V = set()
total_cluster_dfdata = pd.DataFrame()
for batch in result_cursor:
    batchdata = bson.decode_all(batch)  # 编程成文本

    twitter_data = []
    for item in batchdata:
        t1 = item['related_post']['full_text']

        #         t1=item['user_post']['full_text']
        data = {}
        data['_id'] = str(item["_id"])
        data['fulltext'] = t1
        twitter_data.append(data)
    # 将twitter数据转换为Dataframe数据格式
    twitter_data = pd.DataFrame(twitter_data)

    # 分词去停用词等文本处理
    documents, cleaned_fulltext = normalize_corpus(twitter_data)
    print(documents[:5])  # '感觉 威高 广场 见' 这种格式的
    print(cleaned_fulltext[:5])  # 清洗的文本

    # 准备小批次聚类
    texts = [text.split() for text in documents]

    vocab_size, V = compute_V(texts, V)  # 计算词语数

    y = mgp.fit(texts, vocab_size)

    print(y[:10])
    print(Counter(y))

    twitter_data['cleaned_fulltext'] = cleaned_fulltext
    twitter_data['cluster'] = y  # 把得到的类别号存到对应的文章上
    #     print(twitter_data.head())  #打印twitter的数据结构

    # 打印输出聚类结果文本
    num_clusters = len(set(y))

    cluster_data = get_cluster_data(twitter_data, num_clusters)
    print_cluster_data(cluster_data)

    print('A' * 80)

    # 获取聚类后的数据, 格式是 第i篇文章是类别z
    cluster_data = get_cluster_data(twitter_data, num_clusters)

    # 把聚好类的数据，转换成dataframe数据格式
    cluster_dfdata = pd.DataFrame(cluster_data)
    cluster_dfdata_T = cluster_dfdata.T  # 获得矩阵的转置 ，数据格式是 cluster_num，_idCleaned_fulltext

    # 合并每一批次的聚类结果
    if total_cluster_dfdata.empty:
        total_cluster_dfdata = cluster_dfdata_T
    else:

        for i, row in cluster_dfdata_T.iterrows():
            total_cluster_dfdata.iloc[i]['Cleaned_fulltext'].extend(row['Cleaned_fulltext'])
            total_cluster_dfdata.iloc[i]['_id'].extend(row['_id'])

# 使用tf-idf法提取关键词
stopkey = [w.strip() for w in open('./stopwords.txt', 'r', encoding='utf-8').readlines()]
# tf-idf关键词抽取
result = getKeywords_tfidf(total_cluster_dfdata, stopkey, 10)
print(result)