import sys,codecs
import pandas as pd
import numpy as np
import jieba.posseg
import jieba.analyse
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
"""
       TF-IDF权重：
           1、CountVectorizer 构建词频矩阵
           2、TfidfTransformer 构建tfidf权值计算
           3、文本的关键字
           4、对应的tfidf矩阵
"""
# 数据预处理操作：分词，去停用词，词性筛选
def dataPrepos(text, stopkey):
    l = []
    pos = ['n', 'nz', 'v', 'vd', 'vn', 'l', 'a', 'd']  # 定义选取的词性
    seg = jieba.posseg.cut(text)  # 分词
    for i in seg:
        if i.word not in stopkey and i.flag in pos:  # 去停用词 + 词性筛选
            l.append(i.word)
    return l

# tf-idf获取文本top10关键词
def getKeywords_tfidf(data,stopkey,topK):
#     idList, titleList, abstractList = data['id'], data['title'], data['abstract']
    idList,textList,categoryList = data['_id'],data['Cleaned_fulltext'],data['cluster_num']
    corpus = [] # 将所有文档输出到一个list中，一行就是一个文档
    for index in range(len(categoryList)):
#         text = '%s。%s' % (titleList[index], abstractList[index]) # 拼接标题和摘要
        fulltext=''.join(textList[index]).replace(' ','')
        text = dataPrepos(fulltext,stopkey) # 文本预处理
        text = " ".join(text) # 连接成字符串，空格分隔
        corpus.append(text)

    # 1、构建词频矩阵，将文本中的词语转换成词频矩阵
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus) # 词频矩阵,a[i][j]:表示j词在第i个文本中的词频
    # 2、统计每个词的tf-idf权值
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)
    # 3、获取词袋模型中的关键词
    word = vectorizer.get_feature_names()
    # 4、获取tf-idf矩阵，a[i][j]表示j词在i篇文本中的tf-idf权重
    weight = tfidf.toarray()
    # 5、打印词语权重
    ids, keys,texts = [],  [], []
    for i in range(len(weight)):
#        # print("-------这里输出第", i+1 , "篇文本的词语tf-idf------")
        ids.append(idList[i])
        texts.append(textList[i])
#         titles.append(titleList[i])
        df_word,df_weight = [],[] # 当前文章的所有词汇列表、词汇对应权重列表
        for j in range(len(word)):
            # 想在tiidf去除转发作为主题
            if word[j] == "转发":
                continue
            df_word.append(word[j])
            df_weight.append(weight[i][j])
        df_word = pd.DataFrame(df_word,columns=['word'])
        df_weight = pd.DataFrame(df_weight,columns=['weight'])
        word_weight = pd.concat([df_word, df_weight], axis=1) # 拼接词汇列表和权重列表
        word_weight = word_weight.sort_values(by="weight",ascending = False) # 按照权重值降序排列
        keyword = np.array(word_weight['word']) # 选择词汇列并转成数组格式
        word_split = [keyword[x] for x in range(0,topK)] # 抽取前topK个词汇作为关键词
        word_split = " ".join(word_split)
        keys.append(word_split)

    result = pd.DataFrame({"id": ids,  "key": keys, "content":texts},columns=['id','key',"content"])
    return result