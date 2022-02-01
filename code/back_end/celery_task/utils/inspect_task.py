"""
:Inspect the task exist or not
@author: lingzhi
* @date 2021/10/26 11:28
"""
from celery_task.utils import mongo_client
from celery_task.config import mongo_conf


def inspect(tag_task_id: str):
    inspect_result = mongo_client.db[mongo_conf.TASK].find_one({'tag_task_id': tag_task_id})
    if inspect_result:
        pass
    else:
        raise Exception('任务已被删除,抛出异常终止后端异步任务!')
