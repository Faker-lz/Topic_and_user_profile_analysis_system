"""
: 
@author: lingzhi
@time: 2021/7/20 16:09
"""
from pydantic import BaseModel, Field
from datetime import datetime


class TaskCManage(BaseModel):
    tag_task_id: str = Field(None, title='话题任务id',
                             description='由时间戳+tag的MD5构成')
    tag: str = Field(None, title='话题内容',
                     description='搜索的话题关键字')
    tag_celery_task_id: str = Field(None, title='celery任务id',
                                    description='任务执行时生成')
    tag_introduce_id: str = Field(None, title='话题基本信息id',
                                  description='由热度、用户数量等数据组成')
    tag_hot_id: str = Field(None, title='话题热度',
                            description='话题一天、一周、一个月内的热度数据')
    tag_word_cloud_task_id: str = Field(None, title='话题词云id',
                                        description='以分析后的词云为数据项')
    tag_character_task_id: str = Field(None, title='人物角色分类id',
                                       description='依据节点特征对人物进行分类')
    tag_relation_task_id: str = Field(None, title='话题传播关系id',
                                      description='以关系数图据结构为数据项')
    tag_evolve_task_id: str = Field(None, title='tag_evolve_task_id',
                                    description='以演变数据结构为数据项')
    tag_comment_task_id: str = Field(None, title='博文任务id',
                                     description='博文评论分析任务的id')
    status: str = Field(None, title='任务状态')
    tag_create_time: datetime = Field(None, title='创建时间')
