"""
: 任务处理层
@author: lingzhi
@time: 2021/7/19 20:01
"""
from config import *
from celery import Celery, platforms

celeryapp = Celery(__name__,
                   broker='redis://localhost:6379/0',
                   backend='redis://localhost:6379/1',
                   result_serializer=True,)
celeryapp.autodiscover_tasks(['celery_task.task', 'celery_task.tag_comment_task.task.task_schedule',
                              'celery_task.worker', 'celery_task.worker.task_schedule',
                              'celery_task.worker.start_comment_task'])
celeryapp.conf.update(
    result_expires=3600,  # 任务结果一小时内没人取就丢弃
)
platforms.C_FORCE_ROOT = True
