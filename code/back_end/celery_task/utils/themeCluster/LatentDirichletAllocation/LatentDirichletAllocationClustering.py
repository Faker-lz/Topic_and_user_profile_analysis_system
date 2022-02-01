# -*- coding: utf-8 -*-

import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()


class LDAClustering():
    def load_stopwords(self, stopwords_path):
        with open(stopwords_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f]

    def cut_words(self, sentence):
        return ' '.join(jieba.lcut(sentence))

    def pre_process_corpus(self, corpus_path, stopwords_path):
        """
        数据预处理，将语料转换成以词频表示的向量。
        :param corpus_path: 语料路径，每条语料一行进行存放
        :param stopwords_path: 停用词路径
        :return:
        """
        with open(corpus_path, 'r', encoding='utf-8') as f:
            corpus = [self.cut_words(line.strip()) for line in f]

        stopwords = self.load_stopwords(stopwords_path)

        self.cntVector = CountVectorizer(stop_words=stopwords)

        cntTf = self.cntVector.fit_transform(corpus)

        return cntTf

    def fmt_lda_result(self, lda_result):
        ret = {}
        for doc_index, res in enumerate(lda_result):
            li_res = list(res)
            doc_label = li_res.index(max(li_res))
            if doc_label not in ret:
                ret[doc_label] = [doc_index]
            else:
                ret[doc_label].append(doc_index)
        return ret

    def lda(self, corpus_path, n_components=5, learning_method='batch',
            max_iter=10, stopwords_path='../data/stop_words.txt'):
        """
        LDA主题模型
        :param corpus_path: 语料路径
        :param n_topics: 主题数目
        :param learning_method: 学习方法: "batch|online"
        :param max_iter: EM算法迭代次数
        :param stopwords_path: 停用词路径
        :return:
        """
        cntTf = self.pre_process_corpus(corpus_path=corpus_path, stopwords_path=stopwords_path)
        tf_feature_names = self.cntVector.get_feature_names()
        lda = LatentDirichletAllocation(n_components=n_components, max_iter=max_iter, learning_method=learning_method)
        docres = lda.fit_transform(cntTf)

        print_top_words(lda, tf_feature_names, n_top_words=10)

        return self.fmt_lda_result(docres)


if __name__ == '__main__':
    LDA = LDAClustering()
    ret = LDA.lda('../data/test_data2.txt', stopwords_path='../data/stop_words.txt', max_iter=100, n_components=5)
    print(ret)