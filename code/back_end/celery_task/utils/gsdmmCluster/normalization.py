# -*- coding:utf-8 -*-
import re
import os
import string
import jieba

try:
    from .langconv import *
except Exception as e:
    from langconv import *


# 去除中文和英文以外的字符,去除其他国字符
def cleantxt(raw):
    fil = re.compile(u'[^0-9a-zA-Z\u4e00-\u9fa5.，,。“”]+', re.UNICODE)
    return fil.sub(' ', raw)


def filter_emoji(desstr, restr=''):
    # 过滤表情
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


def Traditional2Simplified(sentence):
    '''
    将sentence中的繁体字转为简体字
    :param sentence: 待转换的句子
    :return: 将句子中繁体字转换为简体字之后的句子
    '''
    sentence = Converter('zh-hans').convert(sentence)
    return sentence


# 加载停用词
stopword_list = set()
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'stopwords.txt'), encoding="utf8") as f:
    for line in f:
        item = line.strip()
        stopword_list.add(item)
stopword_list.add("转发")

# 加载色情词
pron_list = set()
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pronography.txt'), encoding="utf8") as f:
    for line in f:
        item = line.strip()
        pron_list.add(item)


def tokenize_text(text):
    tokens = jieba.lcut(text)
    tokens = [token.strip() for token in tokens if len(token.strip()) > 0]
    return tokens


# 去停用词
def remove_stopwords(text):
    tokens = tokenize_text(text)
    filtered_tokens = [token for token in tokens if token not in stopword_list]
    #     filtered_tokens=[]
    # #     flag=True
    #     for token in tokens:
    #         if token not in stopword_list:
    #             filtered_tokens.append(token)
    #         if token in pron_list and flag:
    #             filtered_tokens.append("色情")
    #             flag=False

    return filtered_tokens


def normalize_corpus(twitter_data):
    # 清洗数据
    fulltext = []
    pron_pttn = r"|".join(pron_list)  # 色情词
    url_pattern = re.compile(r'https://[a-zA-Z0-9.?/&=:]*', re.S)  # 过滤网址
    name_pattern = re.compile(r'RT @[a-z,A-Z,0-9,_]+:|@[a-z,A-Z,0-9,_]+')  # 过滤 @微博名
    for item in twitter_data['fulltext']:
        dd = Traditional2Simplified(item)  # 将繁体字转化为中文
        dd = url_pattern.sub("", dd)  # 去除推文后面的链接
        dd = filter_emoji(dd)  # 去除表情
        dd = name_pattern.sub("", dd)
        dd = cleantxt(dd)  # 去除外文
        dd = dd.replace('&amp', '')
        dd = dd.replace('RT', '')
        dd = dd.strip()  # 去除空格
        # isfind=re.search(pron_pttn,dd)#查找色情词汇
        # if isfind is not None:
        #     dd="情色"+dd
        fulltext.append(dd)

    # 去停用词
    normalized_corpus = []

    for text in fulltext:
        #         isfind=re.search(pron_pttn, text)#查找色情词汇
        noStopWords = remove_stopwords(text)

        text = " ".join(noStopWords)
        #         if isfind is not None:
        #             text+=" 色情"
        normalized_corpus.append(text)

    return normalized_corpus, fulltext


def normalize_corpus_part(twitter_data):
    # 清洗数据
    fulltext = []
    pron_pttn = r"|".join(pron_list)  # 色情词
    url_pattern = re.compile(r'https://[a-zA-Z0-9.?/&=:]*', re.S)  # 过滤网址
    name_pattern = re.compile(r'RT @[a-z,A-Z,0-9,_]+:|@[a-z,A-Z,0-9,_]+')  # 过滤 @微博名
    for item in twitter_data:
        dd = Traditional2Simplified(item)  # 将繁体字转化为中文
        dd = url_pattern.sub("", dd)  # 去除推文后面的链接
        dd = filter_emoji(dd)  # 去除表情
        dd = name_pattern.sub("", dd)
        dd = cleantxt(dd)  # 去除外文
        dd = dd.replace('&amp', '')
        dd = dd.replace('RT', '')
        dd = dd.replace('微博', '')
        dd = dd.strip()  # 去除空格
        # isfind=re.search(pron_pttn,dd)#查找色情词汇
        # if isfind is not None:
        #     dd="情色"+dd
        if len(dd) != 0:
            fulltext.append(dd)

    # 去停用词
    normalized_corpus = []

    for text in fulltext:
        #         isfind=re.search(pron_pttn, text)#查找色情词汇
        noStopWords = remove_stopwords(text)

        text = " ".join(noStopWords)
        #         if isfind is not None:
        #             text+=" 色情"
        normalized_corpus.append(text)

    words = []
    for i in normalized_corpus:
        words.append(i.split(' '))
    return words


if __name__ == '__main__':
    print(normalize_corpus_part(['7月17日至18日，由高校书院联盟主办、哈尔滨工业大学（威海）承办的第七届高校现代书院制教育论坛在哈尔滨工业大学（威海）举行。本届论坛以“新时代，新发展——面向未来的书院教育”为主题，近40所高校的300余名专家、师生代表汇聚哈工大（威海），共话现代书院制教育。论坛采用线上线下混合方式举行，另有近200名专家、师生在线听取论坛报告并参与交流，共22.4万人次在线观看。    为期两天的论坛包括3场主旨演讲、9场大会报告、43场分论坛报告、6个圆桌论坛以及穿插其间的书院实地参观、创新创业现场观摩、文化晚会。专家、师生代表围绕“新时代、新发展——面向未来的书院教育”，畅所欲言，互学互鉴，总结交流成功经验，在深入交流中融汇思想，在合作协同中创新理念，共同探索办好高校现代书院的中国方案。    大会共收到来自29所高校的151篇论文。经过评审，56篇论文入选大会论文集，25篇论文获优秀论文奖。    经高校书院联盟理事会会议决议，澳门大学为新一届理事长单位，天津大学天工书院、东南大学健雄书院、西安电子科技大学竹园书院、华东政法大学文伯书院、山西师范大学莳英书院当选为新一批高校书院联盟成员单位。    据悉，成立于2014年的“高校书院联盟”是旨在实现交流合作、资源共享、优势互补、整体提升目的而自愿组成的非营利性组织。联盟成员通过每年一届的高校现代书院制教育论坛共同探索书院制教育模式改革与发展规律，不断满足学生成长成才的需求，提升各联盟成员的书院办学水平、人才培养质量与社会声誉，为培养人格健全、全面发展的创新型人才做出贡献，在世界高等教育舞台上传播中国大学书院制教育的好声音。']))