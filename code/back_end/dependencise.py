"""
: 依赖文件
@author: lingzhi
@time: 2021/7/19 17:21
"""
import motor.motor_asyncio
from celery_task.config.obj import mongo_conf


async def get_mongo_db() -> motor.motor_asyncio.AsyncIOMotorDatabase:
    """
    获取 MongoDB 对象
    """
    client = motor.motor_asyncio.AsyncIOMotorClient(host=mongo_conf.HOST, port=mongo_conf.PORT)
    db = client[mongo_conf.DB_NAME]
    try:
        yield db
    finally:
        client.close()
