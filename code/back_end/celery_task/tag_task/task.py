"""
: 异步任务的定义
@author: lingzhi
@time: 2021/7/19 20:18
"""
from hashlib import md5
from datetime import datetime
import time
from motor.motor_asyncio import AsyncIOMotorDatabase
from celery_task.worker import task_schedule


async def init_task(tag: str, mongo_db: AsyncIOMotorDatabase) -> dict:
    """
    初始化并执行任务
    :param mongo_db: mongo数据库
    :param tag: 话题
    :return: 初始化后生成的任务各部分id
    """
    time_str = str(time.time())  # 当前时间戳
    tag_task_id = md5((time_str + tag).encode('utf-8')).hexdigest()
    task = task_schedule.delay(tag_task_id, tag=tag)
    tag_introduce_id = await mongo_db['tag_introduce'].insert_one({"tag_task_id": tag_task_id})
    tag_hot_id = await mongo_db['tag_hot'].insert_one({"tag_task_id": tag_task_id})
    tag_word_cloud_task = await mongo_db['tag_word_cloud'].insert_one({"tag_task_id": tag_task_id})
    tag_character_task = await mongo_db['character_category'].insert_one({"tag_task_id": tag_task_id})
    tag_relation_task = await mongo_db['tag_relation_graph'].insert_one({"tag_task_id": tag_task_id})
    tag_evolve_task = await mongo_db['tag_evolve'].insert_one({"tag_task_id": tag_task_id})
    tag_weibo_task = await mongo_db['tag_weibo_task'].insert_one({"tag_task_id": tag_task_id})
    tag_user_task = await mongo_db['tag_user'].insert_one({'tag_task_id': tag_task_id})
    tag_create_time = datetime.now()
    # task_init = TaskCManage(tag_task_id=tag_task_id,
    #                         tag_wordcloud_task_id=str(tag_wordcloud_task.inserted_id),
    #                         tag_introduce_id=tag_introduce_id,
    #                         tag_character_task_id=str(tag_character_task.inserted_id),
    #                         tag_relation_task_id=str(tag_relation_task.inserted_id),
    #                         tag_evolve_task_id=str(tag_evolve_task.inserted_id),
    #                         tag_weibo_task_id=str(tag_weibo_task.inserted_id),
    #                         tag_create_time=tag_create_time
    # )
    task_init = {'tag_task_id': tag_task_id,
                 'tag': tag,
                 'tag_celery_task_id': task.id,
                 'tag_word_cloud_task_id': str(tag_word_cloud_task.inserted_id),
                 'tag_hot_task_id': str(tag_hot_id.inserted_id),
                 'tag_introduce_task_id': str(tag_introduce_id.inserted_id),
                 'tag_character_task_id': str(tag_character_task.inserted_id),
                 'tag_relation_task_id': str(tag_relation_task.inserted_id),
                 'tag_evolve_task_id': str(tag_evolve_task.inserted_id),
                 'tag_weibo_task_id': str(tag_weibo_task.inserted_id),
                 'tag_user_id': str(tag_user_task.inserted_id),
                 'status': 'PENDING',
                 'tag_create_time': str(tag_create_time)}
    await mongo_db['tag_task'].insert_one(task_init)

    print(task_init)
    return task_init









