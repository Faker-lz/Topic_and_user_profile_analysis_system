# coding=utf-8

import pickle
from .prepro import preContent
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


def clusterKmeans(task_id):
    corpus = []
    content_comment = preContent()

    # 读取预料 一行预料为一个文档
    for i in content_comment:
        corpus.append(' '.join(i[2]))

    print(corpus)

    # 参考: http://blog.csdn.net/abcjennifer/article/details/23615947
    # vectorizer = HashingVectorizer(n_features = 4000)

    # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
    vectorizer = CountVectorizer()

    # 该类会统计每个词语的tf-idf权值
    transformer = TfidfTransformer()

    # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

    # 获取词袋模型中的所有词语
    word = vectorizer.get_feature_names()
    print("word...")
    print(word)

    # 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
    weight = tfidf.toarray()
    print("weight...")  # list of list格式
    print(weight[200:])

    clf = KMeans(n_clusters=3)  # 景区 动物 人物 国家
    s = clf.fit(weight)
    print(s)

    # print 'Start MiniBatchKmeans:'
    # from sklearn.cluster import MiniBatchKMeans
    # clf = MiniBatchKMeans(n_clusters=20)
    # s = clf.fit(weight)
    # print s

    # 中心点
    # print(clf.cluster_centers_)

    # 每个样本所属的簇
    label = []  # 存储1000个类标 4个类
    print(clf.labels_)
    i = 1
    while i <= len(clf.labels_):
        print(i, clf.labels_[i - 1])
        label.append(clf.labels_[i - 1])
        i = i + 1

    # 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数  958.137281791
    print(clf.inertia_)

    result_dict = {}
    result_dict["cluster1"] = []
    result_dict["cluster2"] = []
    result_dict["cluster3"] = []

    for index, value in enumerate(label):
        print(content_comment[index][1])
        if value == 0:
            result_dict["cluster1"].append(content_comment[index][1])
        elif value == 1:
            result_dict["cluster2"].append(content_comment[index][1])
        elif value == 2:
            result_dict["cluster3"].append(content_comment[index][1])

    return result_dict


if __name__ == "__main__":
    print(clusterKmeans())
