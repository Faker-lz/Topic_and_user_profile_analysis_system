"""
:处理具体博文评论数据的请求
@author: lingzhi
* @date 2021/8/25 17:36
"""
import requests
import re
import signal
from motor.motor_asyncio import AsyncIOMotorDatabase
from celery_task.config import mongo_conf
from celery_task import celeryapp
from dependencise import get_mongo_db


async def get_comment_task_id(tag_task_id: str, weibo_id: str, mongo: AsyncIOMotorDatabase):
    """
    以tag_task_id 获取评论 id
    :param tag_task_id:
    :param weibo_id:
    :param mongo:
    :return:
    """
    comment_task_collection = mongo[mongo_conf.COMMENT_TASK]
    comment_task = await comment_task_collection.find_one({'tag_task_id': tag_task_id, 'weibo_id': weibo_id})
    if comment_task:
        return comment_task.get('tag_comment_task_id')


async def getWeiboById(tag_task_id: str, weibo_id: str, mongo_db: AsyncIOMotorDatabase):
    """
    以id获得微博详细内容
    :param tag_task_id: 话题任务id
    :param weibo_id: 微博id
    :param mongo_db: mongo数据库对象
    :return:
    """
    result = await mongo_db[mongo_conf.COMMENT_TASK].find_one({"tag_task_id": tag_task_id, "weibo_id": weibo_id})
    if result:
        return result['detail']
    return None


async def getByTendencyId(comment_task_id, mongo_db: AsyncIOMotorDatabase):
    """
    以comment_task_id 获取趋势内容
    :param comment_task_id:
    :param mongo_db:
    :return:
    """
    item = await mongo_db[mongo_conf.COMMENT_TENDENCY].find_one({"tag_comment_task_id": comment_task_id})
    if item:
        item.pop("_id")
    else:
        raise
    data_time = []
    data_count = []
    for i in item["data"]:
        if i:
            data_time.append(i["key"])
            data_count.append(i["doc_count"])
    data = {"data_time": data_time, "data_count": data_count}
    item["data"] = data
    return item


async def getByCloudId(comment_task_id, mongo_db: AsyncIOMotorDatabase):
    """
    以comment_task_id 获取词云内容
    :param comment_task_id:
    :param mongo_db:
    :return:
    """
    item = await mongo_db[mongo_conf.COMMENT_CLOUD].find_one({"tag_comment_task_id": comment_task_id})
    if item:
        item.pop("_id")
    return item


def getByClusterId(comment_task_id, mongo_db: AsyncIOMotorDatabase):
    # item = mydb['cluster'].find_one({"task_id": ObjectId(doc_id)})
    item = mongo_db[mongo_conf.COMMENT_CLUSTER].find_one({"tag_comment_task_id": comment_task_id})
    if item:
        item.pop("_id")
    print(item)
    return item


async def getTypeByClusterId(comment_task_id: str, mongo_db: AsyncIOMotorDatabase):
    """
    以comment_task_id 获取 聚类内容
    :param comment_task_id:
    :param mongo_db:
    :return:
    """
    item = await mongo_db[mongo_conf.COMMENT_CLUSTER].find_one({"tag_comment_task_id": comment_task_id})
    if item:
        item.pop("_id")
    result = []
    for i in item['data']:
        key_count = {'key': item['data'][i]['key'],
                     'doc_count': len(item['data'][i]['id'])}
        result.append(key_count)
    return result


# # 以task_id和类别 获取 某一类聚类内容
# async def getPostById(comment_task_id: str, mongo_db: AsyncIOMotorDatabase):
#     item = await mongo_db['task'].find_one({"task_id": task_id})
#     result = []
#     result.append(item["detail"])
#     return result


async def getKeyNode(comment_task_id: str, mongo_db: AsyncIOMotorDatabase):
    item = await mongo_db[mongo_conf.COMMENT_NODE].find_one({"tag_comment_task_id": comment_task_id})
    if item:
        return item['data']


async def get_tree_data(comment_task_id: str, mongo_db: AsyncIOMotorDatabase):
    try:
        data = await mongo_db[mongo_conf.COMMENT_TREE].find_one({'tag_comment_task_id': comment_task_id})
        if data:
            editJson(data['data'])
            return {'tag_comment_task_id': data['tag_comment_task_id'], 'data': data['data']}
    except Exception as e:
        return {"error": str(e)}


async def deleteTask(tag_task_id, mongo_db: AsyncIOMotorDatabase):
    result = mongo_db[mongo_conf.COMMENT_TASK].find({'tag_task_id': tag_task_id})
    comment_task_id_list = list()
    celery_task_id_list = list()
    for i in await result.to_list(length=10):
        comment_task_id_list.append(i['tag_comment_task_id'])
        celery_task_id_list.append(i['celery_id'])
    await mongo_db[mongo_conf.COMMENT_TASK].delete_many({'tag_task_id': tag_task_id})
    for comment_task_id, celery_task_id in zip(comment_task_id_list, celery_task_id_list):
        query = {'tag_comment_task_id': comment_task_id}
        await mongo_db[mongo_conf.COMMENT_CLOUD].delete_one(query)
        await mongo_db[mongo_conf.COMMENT_CLUSTER].delete_one(query)
        await mongo_db[mongo_conf.COMMENT_NODE].delete_one(query)
        await mongo_db[mongo_conf.COMMENT_REPOSTS].delete_many(query)
        await mongo_db[mongo_conf.COMMENT_TENDENCY].delete_one(query)
        await mongo_db[mongo_conf.COMMENT_TREE].delete_one(query)
        celeryapp.control.revoke(celery_task_id, terminate=True, signal=signal.CTRL_C_EVENT)


def editJson(item):
    """
    转换树结构
    :param item:
    :return:
    """
    children_list = [i for i in item["children"].values()]
    item["children"] = children_list
    item["name"] = item.pop("user_name")
    item["value"] = item.pop("content")
    item.pop("user_id")
    for i in item["children"]:
        editJson(i)


if __name__ == '__main__':
    deleteTask('2a135572805cd578edb880394348cbe6', get_mongo_db())
