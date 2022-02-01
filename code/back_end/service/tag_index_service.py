"""
:话题总览页的数据提取服务
@author: lingzhi
* @date 2021/9/16 10:27
"""
from motor.motor_asyncio import AsyncIOMotorDatabase
import signal
from exceptions import NotExistException
from service.get_task_state import get_task_state
from models.dto.tag_dto.introduce_dto import User, ProgressTask, TagBase
from celery_task import celeryapp
from service.comment_extract import deleteTask


async def get_tag_task_list(mongo_db: AsyncIOMotorDatabase) -> list:
    tag_list_find = mongo_db['tag_task'].find({})
    tag_list = list()
    for tag in await tag_list_find.to_list(length=100):
        status = await get_task_state(tag_task_id=tag['tag_task_id'], mongo_db=mongo_db)
        if status == 'SUCCESS':
            tag_base = await mongo_db['tag_introduce'].find_one({'tag_task_id': tag['tag_task_id']})
            if tag_base:
                user = User(
                    **tag_base['vital_user']
                    # user_id=tag_base['vital_user']['user_id'],
                    #         head=tag_base['vital_user']['head'],
                    #         nickname=tag_base['vital_user']['nickname'],
                    #         birthday=tag_base['vital_user']['birthday'],
                    #         verified_reason=tag_base['vital_user']['verified_reason'],
                    #         gender=tag_base['vital_user']['gender'],
                    #         location=tag_base['vital_user']['location'],
                    #         description=tag_base['vital_user']['description'],
                    #         education=tag_base['vital_user']['education'],
                    #         work=tag_base['vital_user']['work'],
                    #         weibo_num=tag_base['vital_user']['weibo_num'],
                    #         following=tag_base['vital_user']['following'],
                    #         followers=tag_base['vital_user']['followers'],
                    #         max_page=tag_base['vital_user']['max_page']
                )
                tag_list.append(TagBase(
                    tag_task_id=tag['tag_task_id'],
                    tag=tag_base['tag'],
                    user_count=tag_base['user_count'],
                    weibo_count=tag_base['weibo_count'],
                    vital_user=user)
                )
        else:
            tag['status'] = status
            tag.pop('_id')
            tag_list.append(ProgressTask(**tag))

    return tag_list


async def get_tag_hot_blog(tag_task_id: str, mongo_db: AsyncIOMotorDatabase) -> list:
    mongo_collection = mongo_db['blog']
    blog_result = await mongo_collection.find_one({'tag_task_id': tag_task_id})
    if blog_result:
        blog_result.pop('_id')
        blog_result['data'] = blog_result['data'][0:10]
        return blog_result['data']
    else:
        raise NotExistException(tag_task_id + '\'s hot_blog')


async def get_word_cloud(tag_task_id: str, mongo_db: AsyncIOMotorDatabase) -> dict:
    mongo_collection = mongo_db['tag_word_cloud']
    word_cloud_result = await mongo_collection.find_one({'tag_task_id': tag_task_id})
    if word_cloud_result:
        word_cloud_result.pop('_id')
    return word_cloud_result


async def get_relation_graph(tag_task_id: str, mongo_db: AsyncIOMotorDatabase) -> dict:
    mongo_collection = mongo_db['tag_relation_graph']
    relation_graph_result = await mongo_collection.find_one({'tag_task_id': tag_task_id})
    if relation_graph_result:
        relation_graph_result.pop('_id')
        for node in relation_graph_result['nodes_list']:
            if 'category' in node.keys():
                node.pop('category')
    return relation_graph_result


async def get_user_mark(tag_task_id: str, mongo_db: AsyncIOMotorDatabase) -> dict:
    mongo_collection = mongo_db['tag_user']
    user_mark_result = await mongo_collection.find_one({'tag_task_id': tag_task_id})
    if user_mark_result:
        user_mark_result.pop('_id')
    return user_mark_result['data']


async def delete_task_by_id(tag_task_id: str, mongo_db: AsyncIOMotorDatabase) -> dict:
    mongo_tag_task_collection = mongo_db['tag_task']
    mongo_character_category_collection = mongo_db['character_category']
    mongo_tag_hot = mongo_db['tag_hot']
    mongo_tag_evolve_collection = mongo_db['tag_evolve']
    mongo_tag_introduce_collection = mongo_db['tag_introduce']
    mongo_tag_relation_collection = mongo_db['tag_relation']
    mongo_tag_weibo_task_collection = mongo_db['tag_weibo_task']
    mongo_tag_word_cloud_collection = mongo_db['tag_word_cloud']
    mongo_tag_user_collection = mongo_db['tag_user']
    mongo_blog_collection = mongo_db['blog']
    task = await mongo_tag_task_collection.find_one({'tag_task_id': tag_task_id})
    if task:
        task.pop('_id')
        try:
            #TODO 修改signal
            celeryapp.control.revoke(task['tag_celery_task_id'], terminate=True, signal=signal.CTRL_C_EVENT)    # 删除后台的一级任务:话题分析任务
            await deleteTask(tag_task_id=tag_task_id, mongo_db=mongo_db)            # 删除后台的二级任务:评论分析任务
            await mongo_character_category_collection.delete_one({'tag_task_id': tag_task_id})
            await mongo_tag_user_collection.delete_one({'tag_task_id': tag_task_id})
            await mongo_tag_hot.delete_one({'tag_task_id': tag_task_id})
            await mongo_tag_evolve_collection.delete_one({'tag_task_id': tag_task_id})
            await mongo_tag_introduce_collection.delete_one({'tag_task_id': tag_task_id})
            await mongo_tag_relation_collection.delete_one({'tag_task_id': tag_task_id})
            await mongo_tag_weibo_task_collection.delete_one({'tag_task_id': tag_task_id})
            await mongo_tag_word_cloud_collection.delete_one({'tag_task_id': tag_task_id})
            await mongo_blog_collection.delete_one({'tag_task_id': tag_task_id})
            await mongo_tag_task_collection.delete_one({'tag_task_id': tag_task_id})
        except Exception as e:
            raise e
        return task
    else:
        raise NotExistException(tag_task_id)
