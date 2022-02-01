"""
:话题转发关系api
@author: lingzhi
* @date 2021/7/23 15:10
"""
from fastapi import APIRouter, Depends
from models.dto.restful_model import RESTfulModel
from dependencise import get_mongo_db
from motor.motor_asyncio import AsyncIOMotorDatabase

retweet = APIRouter(tags=['话题转发关系api'])


@retweet.get('/user_list', response_model=RESTfulModel,
             description='获取该话题人物分类列表')
async def get_user_list(tag_task_id: str, mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    user_result = await mongo_db['tag_user'].find_one({'tag_task_id': tag_task_id})
    if user_result:
        user_result.pop('_id')
    return RESTfulModel(code=0, data=user_result)


@retweet.get('/relation_graph', response_model=RESTfulModel,
             description='转发关系网络图的数据', summary='获取网络图数据')
async def relation_graph(tag_task_id: str, mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    mongo_collection = mongo_db['tag_relation_graph']
    relation_graph_result = await mongo_collection.find_one({'tag_task_id': tag_task_id})
    if relation_graph_result:
        relation_graph_result.pop('_id')
    return RESTfulModel(code=0, data=relation_graph_result)


@retweet.get('/detail_relation_graph', response_model=RESTfulModel,
             description='转发关系网络图的数据', summary='获取网络图数据')
async def get_relation_graph(tag_task_id: str, mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)):
    mongo_collection = mongo_db['tag_relation_graph']
    relation_graph_result = await mongo_collection.find_one({'tag_task_id': tag_task_id})
    if relation_graph_result:
        relation_graph_result.pop('_id')
        relation_graph_result.pop('categories')
    total_hot = 0
    for node in relation_graph_result.get('nodes_list'):
        node['category'] = node.get('category') % 10
        total_hot += node['value'] if node['value'] else 0
    for node in relation_graph_result.get('nodes_list'):
        node['symbolSize'] = node['value']/total_hot * 100
    relation_graph_result['categories'] = list()
    for i in range(10):
        temp = dict({
            'name': str(i)
        })
        relation_graph_result['categories'].append(temp)
    return RESTfulModel(code=0, data=relation_graph_result)

