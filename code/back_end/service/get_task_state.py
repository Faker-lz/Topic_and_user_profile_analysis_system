"""
:获取任务状态
:前端发送获取任务列表请求后，获取并刷新分析状态不为SUCCESS的任务状态信息
@author: lingzhi
* @date 2021/8/14 16:16
"""
from celery_task import celeryapp
from motor.motor_asyncio import AsyncIOMotorDatabase


async def get_task_state(tag_task_id: str, mongo_db: AsyncIOMotorDatabase) -> str:
    """
    获取并刷新task状态信息
    :param mongo_db: mongo数据库
    :param tag_task_id: tag任务id
    :return:
    """
    mongo_collection = mongo_db['tag_task']
    tag_task_result = await mongo_collection.find_one({'tag_task_id': tag_task_id})
    if tag_task_result['status'] != 'SUCCESS':
        if tag_task_result['status'] == 'FAILURE':
            return tag_task_result['status']
        celery_id = tag_task_result['tag_celery_task_id']
        task = celeryapp.AsyncResult(celery_id)
        if task.state == "PROGRESS":
            #   如果任务正在执行,刷新任务状态
            await mongo_collection.update_one({'tag_task_id': tag_task_id},
                                              {'$set': {'status': task.info.get('current', 0)}}
                                              )
            return task.info.get('current', 0)
        else:
            await mongo_collection.update_one({'tag_task_id': tag_task_id},
                                              {'$set': {'status': task.state}}
                                              )
            return task.state
    else:
        return 'SUCCESS'








