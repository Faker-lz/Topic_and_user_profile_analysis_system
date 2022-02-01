from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from dependencise import get_mongo_db
from models.dto.restful_model import RESTfulModel
from celery_task.worker import test
from celery_task.tag_comment_task.task import start_task

test_router = APIRouter(tags=['test'])


@test_router.post('/mongo', response_model=RESTfulModel, summary='测试 MongoDB')
async def mongo_test(mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    mongo_collection = mongo_db['test']
    temp = {'test': 'test'}
    print(temp)
    mongo_resp = await mongo_collection.insert_one(temp)
    print(mongo_resp)
    return RESTfulModel(code=0, data='success')


@test_router.post('/celery', response_model=RESTfulModel, summary='测试 Celery')
async def celery_test(content: str):
    test.delay(content)
    return RESTfulModel(code=0, data='success')


@test_router.get('/tag_user',response_model=RESTfulModel, summary='测试 Celery')
async def celery_user_mark_test(tag_task_id: str, mongo:AsyncIOMotorDatabase = Depends(get_mongo_db)):
    data = await mongo.tag_user.find_one({'tag_task_id': tag_task_id})
    return RESTfulModel(code=0, data=data.get('data'))






