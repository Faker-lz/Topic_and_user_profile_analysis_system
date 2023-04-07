"""
:话题爬虫任务
@author: lingzhi
* @date 2021/7/22 16:24
"""

import requests
import json
from celery_task.utils import mongo_client
from celery_task.utils.my_cloud import MyCloud
from celery_task.config import mongo_conf
from celery_task.utils.gopup_utils import user


def spider(tag: str, tag_task_id: str):
    """
    tag微博数据的爬取与储存
    :param tag_task_id: 任务id
    :param tag: 话题
    :return:
    """
    result_data_list = list()
    user_set = set()
    false_count = 0     # 无效请求次数
    for i in range(1, 50, 1):
        if false_count >= 5:
            break       # 无效请求大于等于5时,认为无法得到相关数据，停止请求
        url = 'http://127.0.0.1:8000/weibo_curl/api/search_tweets?keyword={keyword}&cursor={cursor}&is_hot=1' \
            .format(keyword=tag, cursor=i)
        response = requests.get(url)
        print(url)
        print('false_count: %s' % false_count)
        weibo_dict = json.loads(response.text)
        if weibo_dict['error_code'] == 0:
            false_count = 0
            weibo_list = weibo_dict.get('data').get('result')
            new_weibo_list = list()
            for weibo in weibo_list:
                weibo['text'] = weibo['text'] + ' '
                weibo['tid'] = weibo['weibo_id']
                weibo['text_token'] = MyCloud(weibo['text'].split(' ')).GetKeyWord()
                weibo['retweet_count'] = weibo.pop('reposts_count')
                weibo['favorite_count'] = weibo.pop('attitudes_count')
                weibo['comment_count'] = weibo.pop('comments_count')
                weibo['tweet_type'] = 'article'
                weibo['data_source'] = 'weibo'
                weibo['hot_count'] = int(weibo['retweet_count']) + int(weibo['favorite_count']) + int(weibo['comment_count'])
                user_set.add(weibo['user_id'])
                new_weibo_list.append(weibo)
            result_data_list.extend(new_weibo_list)
        else:
            false_count += 1
    result_data_list.sort(key=lambda x: int(x['hot_count']), reverse=True)
    result_data_dict = dict()
    result_data_dict['data'] = result_data_list
    result_data_dict['tag'] = tag
    result_data_dict['tag_task_id'] = tag_task_id
    weibo_id_set = set()              # 热度排名前十的weibo_id
    weibo_post_list = list()
    for i in range(0, len(result_data_dict['data']), 1):
        if result_data_dict['data'][i]['weibo_id'] not in weibo_id_set:
            weibo_post_list.append(result_data_dict['data'][i])
            weibo_id_set.add(result_data_dict['data'][i]['weibo_id'])
        if len(weibo_id_set) >= 10:
            break
    mongo_client.db[mongo_conf.BLOG].insert_one(result_data_dict)
    return result_data_dict, list(weibo_post_list), list(user_set)
