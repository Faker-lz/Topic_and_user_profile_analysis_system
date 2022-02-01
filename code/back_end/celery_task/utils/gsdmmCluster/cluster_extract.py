import re
import time
import pymongo
import pandas as pd
from collections import Counter

try:
    from .mgp import MovieGroupProcess
    from .normalization import normalize_corpus
    from .tfidf import getKeywords_tfidf
except Exception as e:
    from mgp import MovieGroupProcess
    from normalization import normalize_corpus
    from tfidf import getKeywords_tfidf

import sys, codecs

import os

stopwords_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stopwords.txt')


# 计算词语数
def compute_V(texts):
    V = set()
    for text in texts:
        for word in text:
            V.add(word)
    return len(V)


# 获取每一簇的数据
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

    return cluster_details


def print_cluster_data(cluster_data):
    # print cluster details
    for cluster_num, cluster_details in cluster_data.items():
        pass
    # print'Cluster{} details'.format(cluster_num))
    # print'-'*20)


#        # print'Key features:',cluster_details['key_features'])
# print'sentence in this clusters:')
# print'>'.join(cluster_details['Cleaned_fulltext'][:30]).replace('\n',''))
# print'='*40)


# client = pymongo.MongoClient('mongodb://10.245.142.249:27017/')
# mdb = client['person_scout_all']
client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
mdb = client['weibo_sjy']


def cluster_extract(post_list):
    twitter_data = pd.DataFrame(post_list)
    if twitter_data.get('fulltext') is None:
        return
    documents, cleaned_fulltext = normalize_corpus(twitter_data)  # 做数据清洗，并处理成对应的格式
    twitter_data['cleaned_fulltext'] = cleaned_fulltext

    # 2.聚类
    texts = [text.split() for text in documents]
    V = compute_V(texts)

    # 设置初始聚类数K为6
    mgp = MovieGroupProcess(K=6, alpha=0.01, beta=0.02, n_iters=60)
    y = mgp.fit(texts, V)  # 聚类结果
    # print"每一类聚的推文数：",Counter(y))
    twitter_data['cluster'] = y  # 把聚类结果添加到DataFrame数据中
    print(twitter_data)

    # 3.关键词提取
    num_clusters = len(set(y))  # 获取聚类后的簇数
    # 获取聚类后的数据
    cluster_data = get_cluster_data(twitter_data, num_clusters)

    # -----打印聚类后的数据----
    print_cluster_data(cluster_data)  # 可注释本行代码

    # 把聚好类的数据，转换成dataframe数据格式
    cluster_dfdata = pd.DataFrame(cluster_data)
    cluster_dfdata_T = cluster_dfdata.T  # 获得矩阵的转置

    # 3.使用tf-idf法提取关键词

    stopkey = [w.strip() for w in codecs.open(stopwords_path, 'rb').readlines()]
    # tf-idf关键词抽取
    result = getKeywords_tfidf(cluster_dfdata_T, stopkey, 3)

    return result


def run_by_id(event_id):
    ## printtype(event_id))
    ## printevent_id)
    # while True:
    # for event in mdb['event'].find():

    post_list = []

    for post in mdb['event_post_weibo'].find({'event_id': event_id}):
        post_list.append({'_id': str(post['related_post']['id_str']), 'fulltext': post['related_post']['full_text']})
    for post in mdb['event_post'].find({'event_id': event_id}):
        post_list.append({'_id': str(post['related_post']['id_str']), 'fulltext': post['related_post']['full_text']})

    if post_list:
        result = cluster_extract(post_list)
        if result:
            mdb['event_classify'].remove({'event_id': event_id})
            for row in result.itertuples(index=True, name='Pandas'):
                data = {'event_id': event_id, 'keyword': getattr(row, "key"), 'posts': getattr(row, "id"),
                        'spread_analysis': False}
                mdb['event_classify'].insert_one(data)
        else:
            print('No fulltext is None!!!')




def run_by_id_str(person_id, source):
    # printtype(person_id))
    # printperson_id)
    post_list = []

    if source == 'twitter':
        doc = 'person_post'
    elif source == 'weibo':
        doc = 'person_post_weibo'
    for post in mdb[doc].find({'person_id': person_id}):
        post_list.append({'_id': str(post['person_post']['id_str']), 'fulltext': post['person_post']['full_text']})

    if post_list:

        result = cluster_extract(post_list)
        mdb['person_classify'].remove({'person_id': person_id})
        for row in result.itertuples(index=True, name='Pandas'):
            data = {'person_id': person_id, 'keyword': getattr(row, "key"), 'posts': getattr(row, "id"),
                    'spread_analysis': False}
            mdb['person_classify'].insert_one(data)


import datetime


def run_by_time():
    time_range = [750, 1200, 1700]
    while True:
        time.sleep(60 * 5)
        date_time = datetime.datetime.now()
        now_time = date_time.hour * 100 + date_time.minute
        for i in time_range:
            if now_time - i > 5:
                continue
        for event in mdb['event'].find():
            run_by_id(event['_id'])

# 任务进入接口
def run_by_task_id(task_id):
    post_list = []
    for post in mdb['Reposts'].find({'task_id': task_id}):
        if post['content'].strip() == "" or post['content'].strip() == "转发微博":
            continue
        post_list.append({'_id': post['_id'], 'fulltext': post['content']})
    print(len(post_list))
    result = cluster_extract(post_list)
    mydict = result.to_dict(orient='index')
    key_list = list(mydict.keys())
    for key in key_list:
        mydict[str(key)] = mydict.pop(key)
        while '' in mydict[str(key)]["content"]:
            mydict[str(key)]["content"].remove('')
    obid = mdb['cluster'].insert_one(mydict)
    return obid.__str__()




if __name__ == '__main__':
    from bson import ObjectId

    # run_by_time()
    ## printrun_by_id(ObjectId("5db6abe0c03558516c2632a8")))
    run_by_task_id('111')
