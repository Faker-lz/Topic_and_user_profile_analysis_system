"""
: 博文详细页请求的api
@author: lingzhi
@time: 2021/7/20 15:27
"""
from fastapi import APIRouter, Depends
from models.dto.restful_model import RESTfulModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from dependencise import get_mongo_db
from service.comment_extract import get_tree_data, get_comment_task_id, getByTendencyId, getByCloudId,\
    getTypeByClusterId, getKeyNode, getWeiboById

comment_router = APIRouter(tags=['微博评论分析api'])


@comment_router.get('/post_detail', response_model=RESTfulModel,
                    description='获取文章详细信息',
                    summary='文章')
async def get_post_detail(tag_task_id: str, weibo_id: str, mongo: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    return RESTfulModel(code=0, data=await getWeiboById(tag_task_id=tag_task_id, weibo_id=weibo_id, mongo_db=mongo))


@comment_router.get('/tree', response_model=RESTfulModel,
                    description='获取微博传播树结果',
                    summary='传播树')
async def get_tree(tag_task_id: str, weibo_id: str, mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    comment_task_id = await get_comment_task_id(tag_task_id=tag_task_id, weibo_id=weibo_id, mongo=mongo_db)
    try:
        return RESTfulModel(code=0, data=await get_tree_data(comment_task_id, mongo_db))
    except Exception as e:
        return RESTfulModel(code=1, data=str(e))


@comment_router.get('/tendency', response_model=RESTfulModel,
                    description='获取微博热度趋势数据',
                    summary='热度数据')
async def get_tendency(tag_task_id: str, weibo_id: str, mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    comment_task_id = await get_comment_task_id(tag_task_id=tag_task_id, weibo_id=weibo_id, mongo=mongo_db)
    return RESTfulModel(code=0, data=await getByTendencyId(comment_task_id, mongo_db))


@comment_router.get('/cloud', response_model=RESTfulModel,
                    description='获取评论云图数据',
                    summary='云图数据')
async def get_cloud(tag_task_id: str, weibo_id: str, mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    comment_task_id = await get_comment_task_id(tag_task_id=tag_task_id, weibo_id=weibo_id, mongo=mongo_db)
    return RESTfulModel(code=0, data=await getByCloudId(comment_task_id, mongo_db))


@comment_router.get('/cluster/type', response_model=RESTfulModel,
                    description='获取评论聚类数据',
                    summary='聚类')
async def get_cluster(tag_task_id: str, weibo_id: str, mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    comment_task_id = await get_comment_task_id(tag_task_id=tag_task_id, weibo_id=weibo_id, mongo=mongo_db)
    return RESTfulModel(code=0, data=await getTypeByClusterId(comment_task_id, mongo_db=mongo_db))


@comment_router.get('/key_node', response_model=RESTfulModel,
                    description='获取评论中的关键节点',
                    summary='关键节点')
async def get_key_node(tag_task_id: str, weibo_id: str, mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    comment_task_id = await get_comment_task_id(tag_task_id=tag_task_id, weibo_id=weibo_id, mongo=mongo_db)
    return RESTfulModel(code=0, data=await getKeyNode(comment_task_id, mongo_db))



