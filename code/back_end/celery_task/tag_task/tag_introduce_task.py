"""
:话题基本信息任务构建
@author: lingzhi
* @date 2021/8/8 10:44
"""

from celery_task.config import mongo_conf
from celery_task.utils import mongo_client
from celery_task.utils.gopup_utils import user
import requests
import json


def introduce(tag_data: dict, tag_task_id: str):
    """

    :param tag_task_id: 话题任务id
    :param tag_data: 话题下的微博数据
    :return:
    """
    data_list = tag_data['data']
    weibo_count = len(data_list)         # 微博数
    weibo_userid = set()                 # 用户集合
    vital_user_id = str()                # 用户id
    hot = 0
    for weibo in data_list:
        weibo_userid.add(weibo['weibo_id'])
        if int(weibo['hot_count']) > hot:
            vital_user_id = weibo['user_id']
            hot = int(weibo['hot_count'])
    vital_user = get_user_data(vital_user_id)
    tag_introduce_dict = {'tag_task_id': tag_task_id,
                          'tag': tag_data['tag'],
                          'user_count': len(weibo_userid),
                          'weibo_count': weibo_count,
                          'vital_user': vital_user}
    query_by_task_id = {'tag_task_id': tag_task_id}
    update_data = {"$set": tag_introduce_dict}
    mongo_client.db[mongo_conf.INTRODUCE].update_one(query_by_task_id, update_data)
    # with Mongo('tag_introduce', 'test') as mongo_db:
    #     mongo_db.collect.update_one(query_by_task_id, update_data)


def get_user_data(user_id) -> json:
    """
    获取user详细信息
    :param user_id:微博user_id
    :return:
    """
    url = f'http://127.0.0.1:8000/weibo_curl/api/users_show?user_id={user_id}'
    response = requests.get(url)
    response_dict = json.loads(response.text)
    if response_dict.get('data'):
        user_dict = response_dict.get('data').get('result')
        return user_dict
    else:
        return user(user_id)
