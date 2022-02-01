"""
:话题初始页及查询页的api
@author: lingzhi
* @date 2021/7/21 16:37
"""
import json

import requests
from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from exceptions import NotExistException
from dependencise import get_mongo_db
from models.dto.restful_model import RESTfulModel
from models.dto.tag_dto.introduce_dto import TagBase, User, ProgressTask
from service.tag_hot_extract import update_hot_data
from service.get_task_state import get_task_state
from config import weibo_conf
from celery_task.tag_task.task import init_task
from celery_task.worker import start_task
from service.tag_index_service import get_tag_task_list, get_tag_hot_blog, delete_task_by_id, get_word_cloud, \
    get_relation_graph, get_user_mark


tag_router = APIRouter(tags=['话题总览页api'])

@tag_router.get('/tag_list',
                response_model=RESTfulModel,
                description='获取当前的tag_list',
                summary='获取话题列表'
                )
async def tag_list_get(mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    tag_list = await get_tag_task_list(mongo_db)
    return RESTfulModel(code=0, data=tag_list)


@tag_router.get('/delete_task', response_model=RESTfulModel,
                description='删除任务',
                summary='删除指定任务')
async def delete_task(tag_task_id: str, mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    try:
        task = await delete_task_by_id(tag_task_id, mongo_db)
    except NotExistException as e:
        return RESTfulModel(code=-1, data=e.msg)
    return RESTfulModel(code=0, data=task)


@tag_router.get('/blog_rank',
                response_model=RESTfulModel,
                description='获取选中话题博文热度排名',
                summary='获取Tag中热度前十的博文')
async def blog_rank(tag_task_id: str, mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    try:
        blog_result = await get_tag_hot_blog(tag_task_id, mongo_db)
    except NotExistException as exc:
        raise exc
    return RESTfulModel(code=0, data=blog_result)


@tag_router.get('/hot', response_model=RESTfulModel,
                description='获取该话题在一天内、一个月内、三个月内的热度数据',
                summary='话题热度发展的数据')
async def hot(tag_task_id: str, mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    data = await update_hot_data(tag_task_id=tag_task_id, mongo_db=mongo_db)
    return RESTfulModel(code=0, data=data)


@tag_router.get('/word_cloud', response_model=RESTfulModel,
                description='词云的数据', summary='获取词云')
async def word_cloud(tag_task_id: str, mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    word_cloud_result = await get_word_cloud(tag_task_id, mongo_db)
    return RESTfulModel(code=0, data=word_cloud_result)


@tag_router.get('/relation_graph', response_model=RESTfulModel,
                description='网络图的数据', summary='获取网络图数据')
async def relation_graph(tag_task_id: str, mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    relation_graph_result = await get_relation_graph(tag_task_id, mongo_db)
    return RESTfulModel(code=0, data=relation_graph_result)


@tag_router.get('/search', response_model=RESTfulModel,
                description='搜索', summary='搜索某一话题')
def search(tag: str, cursor: int):
    url = weibo_conf.BASEPATH + '/weibo_curl/api/search_tweets?keyword={keyword}&cursor={cursor}&is_hot=1' \
        .format(keyword=tag, cursor=cursor)
    response = requests.get(url)
    weibo_dict = json.loads(response.text).get('data')
    return RESTfulModel(code=0, data=weibo_dict)


@tag_router.get('/add_task', response_model=RESTfulModel,
                description='添加任务', summary='添加该话题到任务队列中',
                status_code=status.HTTP_201_CREATED)
async def add_task(tag: str, mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    init_result = await init_task(tag, mongo_db)
    if init_result:
        init_result.pop('_id')
    return RESTfulModel(code=0, data=init_result)


@tag_router.get('/user_mark', response_model=RESTfulModel,
                description='用户标签', summary='获取用户标签数据')
async def user_mark(tag_task_id: str, mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    user_mark_result = await get_user_mark(tag_task_id=tag_task_id, mongo_db=mongo_db)
    return RESTfulModel(code=0, data=user_mark_result)


@tag_router.get('/get_detail_blog', response_model=RESTfulModel, summary='获取并分析某位用户的所有微博')
async def get_detail_blog(user_id: str, tag_task_id: str, mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    blog = list()
    for i in range(1, 11, 1):
        url = 'http://127.0.0.1:8000/weibo_curl/api/statuses_user_timeline?user_id={user_id}&cursor={i}'\
            .format(user_id=user_id, i=i)
        print(url)
        response = requests.get(url)
        data = json.loads(response.text)
        print(data)
        if data['error_code'] == 0:
            blog.extend(data['data']['result']['weibos'])
            for weibo in data['data']['result']['weibos']:
                start_task(tag_task_id, weibo)
    mongo_db['detail_blog'].insert_many(blog)



