"""
:词云构建工具
@author: lingzhi
* @date 2021/8/10 15:51
"""

# -*- coding: utf-8 -*
# from tfidfCluster.langconv import *        # 目前没有用到该算法
from .gsdmmCluster.normalization import normalize_corpus_part
import pymongo
import os


class MyCloud:
    def __init__(self, content: list):
        self.content = content
        # TODO path
        self.stop_words = [w.strip() for w in open('E:\study\lab\大二年度项目\yuqing_fastapi\src\dict\哈工大停用词表.txt', 'r', encoding='UTF-8').readlines()]
        self.words_list = list()  # 分词表
        self.words_dict = dict()  # 词语和对应出现次数 字典

    def Sent2Word(self):
        """
        对文本进行分词,并将分词列表中的 停用词去掉
        """
        self.words_list = normalize_corpus_part(self.content)
        self.words_list = [w for w in self.words_list if w not in self.stop_words]

    def CountWords(self):
        """
        对分词列表中的词语进行统计
        """
        for words in self.words_list:
            for word in words:
                if len(word) == 0 or word == '':
                    continue
                elif word not in self.words_dict.keys():
                    self.words_dict[word] = 1
                else:
                    self.words_dict[word] += 1

    def ReshapeDict(self):
        """
        改变形式self.words_dict + 排序
        :return:
        """
        words_list = []
        for key in self.words_dict:
            if len(key) >=2:
                item = dict()
                item['name'] = key
                item['value'] = self.words_dict[key]
                words_list.append(item)
        self.words_list = words_list
        self.words_list.sort(key=lambda i: i['value'], reverse=True)

    def GenerateWordCloud(self):
        """
        生成词云
        :return:
        """
        self.Sent2Word()
        self.CountWords()
        self.ReshapeDict()


    def GetWordCloud(self):
        """
        最终的词云数据
        :return: 最终的词云数据
        """
        self.GenerateWordCloud()
        return self.words_list

    def GetKeyWord(self):
        """
        将构建完成的词云关键字返回
        :return:
        """
        self.GenerateWordCloud()
        key_word = str()
        for i in range(0, len(self.words_list), 1):
            if i < len(self.words_list):
                key_word = key_word + self.words_list[i]['name'] + ' '
            else:
                key_word = key_word + self.words_list[i]['name']
            if i >= 30:
                break
        return key_word

if __name__ == "__main__":
    client = pymongo.MongoClient()
    mongo_db = client.test
    collection = mongo_db.blog
    result = collection.find_one({'tag_task_id': '67ff296d200895e0effc2482273b311f'})
    weibo_list = list()
    for i in result.get('data'):
        weibo_list.append(i.get('text'))
    cloud_list = MyCloud(weibo_list).GetWordCloud()
    print(cloud_list)

