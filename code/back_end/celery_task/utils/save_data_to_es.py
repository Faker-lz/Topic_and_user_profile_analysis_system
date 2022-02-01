# coding:utf-8
"""
:将爬取到的微博数据保存到es里
@author: lingzhi
* @date 2021/8/30 10:16
"""
import asyncio
from elasticsearch.helpers import async_bulk
import datetime
import traceback
from elasticsearch import AsyncElasticsearch
from tornado import gen

from celery_task.config import es_conf, LOGGING, mongo_conf, APM
from celery_task.utils import mongo_client


ES_CLIENT = AsyncElasticsearch(hosts=es_conf.ES_HOST, sniff_on_start=True,
                               sniff_on_connection_fail=True, sniffer_timeout=es_conf.ES_TIMEOUT, verify_certs=False,
                               ssl_show_warn=False)


@gen.coroutine
def insert_doc(index_name_list, tid_list, doc_list):
    def gendata():
        for i in range(len(tid_list)):
            action = {
                '_op_type': 'index',
                '_index': 'weibo',
                '_id': tid_list[i],
                '_source': doc_list[i]
            }
            yield action
    result = yield async_bulk(ES_CLIENT, gendata())
    print('**')
    for i in result:
        print(i)
    return result


# 数据保存  es
@gen.coroutine
def general_save_es_bulk(es_db, data_formated_list, _id='_id', retry_time=2):
    print('hello')
    if not data_formated_list:
        LOGGING.info('es save bulk: no data to save', extra={'params': None})
        return True
    index_name_list = []
    tid_list = []
    doc_list = []
    for data_formated in data_formated_list:
        print(data_formated)
        # 设置es的index，去掉30day以前的数据，设置用于es按语言索引的字段text_index_lang
        created_at = data_formated['created_at'][:10].replace('-', '.')
        es_db_tmp = '%s-%s' % (es_db, created_at)
        if (datetime.datetime.now() - datetime.datetime.strptime(created_at, '%Y.%m.%d')).days > 30:
            continue
        data_formated['text_index_' + 'zh'] = data_formated['text']

        index_name_list.append(es_db_tmp)
        tid_list.append(data_formated[_id])
        doc_list.append(data_formated)

    if doc_list:
        for i in range(retry_time):
            # try:
            response = yield insert_doc(index_name_list, tid_list, doc_list)
            LOGGING.info('es save success',
                         extra={'params': None,
                                'data_count': len(data_formated_list)})
            print(response)
            return True
            # except Exception as e:
            #     e_info = traceback.format_exc()
            #     LOGGING.warning('es save error, wait for retry',
            #                     extra={'params': None,
            #                            'data_count': len(data_formated_list),
            #                            'es_host': es_conf.ES_HOST,
            #                            'es_db': es_db,
            #                            'error_msg': e_info})
            #     APM.client.capture_exception()
        APM.client.capture_message('ES save FAILD with %s times' % retry_time)
        LOGGING.critical('ES SAVE ERROR!!! CHECK ES`s STATUS NOW!',
                         extra={'params': None,
                                'data_count': len(data_formated_list),
                                'es_host': es_conf.ES_HOST,
                                'es_db': es_db})
        return False


if __name__ == '__main__':
    weibo_list = mongo_client.db[mongo_conf.BLOG].find_one({"tag_task_id": "51379c82bae2a2499d49ed75c6f12e56"})['data']
    # print(weibo_list)
    # weibo_list = [{'head': 'https://tvax3.sinaimg.cn/crop.0.0.1080.1080.50/9f70e9c4ly8ge4lf6oz37j20u00u0jte.jpg?KID='
    #                        'imgbed,tva&Expires=1630395696&ssig=5acRVO%2BV5N','tid': 'Kvpz1BJFS', 'weibo_id': 'Kvpz1BJFS'
    #                   , 'user_id': '2674977220', 'followers_count': 378695, 'screen_name': '网易娱乐频道', 'text': '#一张图看懂娱乐圈的资本局#在#赵薇接连退出多家公司#之后，明星艺人们的商业联系也引发网友关注。据天眼查APP资料显示，部分明星的商业版图如下↓ ', 'article_url': '', 'location': '', 'at_users': [], 'topics': '一张图看懂娱乐圈的资本局,赵薇接连退出多家公司', 'reposts_count': '18486', 'comments_count': '39109', 'attitudes_count': '1025639', 'created_at': '2021-08-27 17:53', 'source': '微博 weibo.com', 'pics': ['http://ww4.sinaimg.cn/large/002V1VLSly1gtvhx4l73kj62ow4ot1ky02.jpg'], 'video_url': '', 'retweet_id': '', 'hot_count': '1083234', 'text_token': '明星 商业 一张 图看 懂 娱乐圈 资本 局 赵薇 接连 退出 多家 公司 之后 艺 联系 引发 网友 关注 天眼 查 APP 资料 显示 部分 版图 ', 'retweet_count': 5290, 'comment_count':5692, 'tweet_type':'article', 'favorite_count': 59187, 'data_source':'weibo', }]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(general_save_es_bulk(es_conf.ES_SEARCH_INDEX, weibo_list, 'weibo_id'))
    # result = general_save_es_bulk(es_conf.ES_SEARCH_INDEX, weibo_list, 'weibo_id')
    # for i in result:
    #     print(i)
