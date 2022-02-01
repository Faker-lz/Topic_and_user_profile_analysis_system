"""
:
@author: lingzhi
* @date 2021/8/7 9:48
"""
import time

from celery_task import celeryapp
from celery_task.tag_task.tag_spider_task import spider
from celery import current_task
from celery_task.tag_task.tag_introduce_task import introduce
from celery_task.tag_task.tag_word_cloud_task import word_cloud
from celery_task.tag_task.tag_relaton_task import tag_relation
from celery_task.tag_task.tag_hot_task import hot_task
from celery_task.utils.update_task_status import update_task_status
from celery_task.tag_comment_task.task import start_task
from celery_task.tag_task.tag_user_analysis_task import user_analysis
from celery_task.config import mongo_conf


@celeryapp.task()
def task_schedule(tag_task_id: str, tag: str):
    """
    任务管理函数
    :param tag_task_id: 话题任务id
    :param tag:话题名
    :param task_id_dict:各个任务id组成的字典
    :return:
    """

    print('开始爬虫任务')
    current_task.update_state(state='PROGRESS',
                              meta={'current': "爬虫任务", 'task_id': tag_task_id})
    update_task_status(tag_task_id, 'PROGRESS')
    weibo_data, weibo_post_list, user_id_list = spider(tag, tag_task_id)

    print('开始构建话题基本信息任务')
    current_task.update_state(state='PROGRESS',
                              meta={'current': "构建话题基本信息", 'task_id': tag_task_id})
    introduce(weibo_data, tag_task_id)

    print('开始构建词云任务')
    current_task.update_state(state='PROGRESS',
                              meta={'current': "构建词云任务", 'task_id': tag_task_id})
    word_cloud(weibo_data, tag_task_id)

    # 开始爬取详细博文任务, 由于分析用户成分任务阻塞时间较长，故而在此处发布博文详细任务的提取
    start_comment_task.delay(weibo_post_list, tag_task_id)

    print('分析用户成分任务')
    current_task.update_state(state='PROGRESS',
                              meta={'current': '分析用户成分任务', 'task_id': tag_task_id})
    user_mark_data = user_analysis(weibo_data, tag_task_id, user_id_list)

    print('开始构建转发关系任务')
    current_task.update_state(state='PROGRESS',
                              meta={'current': "构建转发关系任务", 'task_id': tag_task_id})
    tag_relation(weibo_data, tag_task_id, user_mark_data)

    print('开始挖掘热度数据任务')
    current_task.update_state(state='PROGRESS',
                              meta={'current': "挖掘热度信息任务", 'task_id': tag_task_id})
    hot_task(weibo_data['tag'], tag_task_id)

    current_task.update_state(state='SUCCESS',
                              meta={'current': "完成", 'task_id': tag_task_id})
    update_task_status(tag_task_id, 'SUCCESS')


@celeryapp.task()
def start_comment_task(weibo_post_list: list, tag_task_id):
    """
    微博评论分析任务
    :param weibo_post_list: 要分析的博文详细信息
    :param tag_task_id: 任务id
    :return:
    """
    for weibo_post in weibo_post_list:
        start_task(tag_task_id=tag_task_id, weibo_post=weibo_post)
        time.sleep(3)


@celeryapp.task()
def test(content: str):
    while True:
        print(content)

#6616523296
