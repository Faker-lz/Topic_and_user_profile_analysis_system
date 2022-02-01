"""
:用户分析任务
@author: lingzhi
* @date 2021/10/23 23:26
"""
from celery_task.utils.gopup_utils import tendency
from celery_task.utils.my_db import Mongo
import requests
import json
from celery_task.utils.themeCluster.Single_Pass.single_pass_cluster import SinglePassCluster
from celery_task.utils.gopup_utils import user
import random
import time


def user_analysis(weibo_blog_data: dict, tag_task_id: str, user_id_list: list):
    user_list = list()
    for user_id in user_id_list:
        try:
            user_url = 'http://127.0.0.1:8000/weibo_curl/api/users_show?user_id={user_id}'.format(user_id=user_id)
            print(f'爬取:{user_id}用户')
            user_dict = json.loads(requests.get(user_url).text)
            if user_dict['error_code'] == 0:
                user_list.append(user_dict.get('data').get('result'))
            else:
                user_list.append(user(user_id))
        except :
            print(f'user_id={user_id},用户信息爬取失败')
            time.sleep(random.uniform(5, 15))
    user_mark = SinglePassCluster(tag_task_id=tag_task_id, blog_data=weibo_blog_data.get('data'),
                                  user_list=user_list)
    user_mark_data = user_mark.single_pass()
    return user_mark_data
