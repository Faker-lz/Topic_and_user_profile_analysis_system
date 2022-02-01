"""
: 
@author: lingzhi
@time: 2021/7/20 17:32
"""
from pydantic import BaseModel, Field
from typing import List
from ..character_dto.character_category import Category


class Node(BaseModel):
    category: Category = Field(2, title='类别')
    name: str = Field(None, title='名称')
    value: int = Field(None, title='节点的大小')


class Link(BaseModel):
    source: str = Field(None, title='源', description='来源方')
    target: str = Field(None, title='目标', description='转发方')
    weight: int = Field(None, title='权值', description='重要程度')


class RelationGraph(BaseModel):
    tag_task_id: str = Field(None, title='话题任务id',
                             description='由时间戳+tag的MD5构成')
    tag_relation_task_id: str = Field(None, title='关系连接图的id')
    node_list: List[Node] = Field(None, title='用户节点列表',
                            description='每个元素由categoty(类别，用123表示)、name（用户昵称）、value（节点大小）组成')
    #   如{\'category\': 2, \'name\': \'港口不察', 'value': 0}
    links_list: List[Link] = Field(None, title='连接列表',
                             description='每个元素由source、target、weight组成的列表')
    #   如{'source': '一位不愿透露姓名的保安', 'target': '一位不愿透露姓名的保安', 'weight': 8}

