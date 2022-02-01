"""
: 话题演变的数据结构
@author: lingzhi
@time: 2021/7/20 17:51
"""
from pydantic import BaseModel, Field
from ..character_dto.character_category import Category
from typing import List
from datetime import datetime


class WeiBo(BaseModel):
    weibo_id: str = Field(None, title='微博的id', description='后续用来查找对应的微博')
    content: str = Field(None, title='博文内容', description='直接在右边展示的内容')


class Cluster(BaseModel):
    cluster_name: str = Field(None, title='簇的名字', description='聚类后的类名')
    weibo_list: List[WeiBo] = Field(None, title='簇内的微博列表', description='聚类后该类别下的微博')


class Time(BaseModel):
    time: datetime = Field(None, title='时间节点', description='话题演变的时间节点')
    cluster_list: List[Cluster] = Field(None, title='簇列表', description='该时间节点下的簇列表')


class Evolve(BaseModel):
    tag_task_id: str = Field(None, title='话题任务id',
                             description='由时间戳+tag的MD5构成')
    category: Category = Field(2, title='任务类别', description='和任务分类数据结构中一一对应')
    time_list: List[Time] = Field(None, title='时间节点列表', description='话题的时间节点列表，内含簇列表和对应的微博信息')
