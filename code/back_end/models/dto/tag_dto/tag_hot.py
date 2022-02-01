"""
:话题热度dto
@author: lingzhi
* @date 2021/8/13 15:17
"""
from pydantic import BaseModel, Field
from typing import List


class TagHot(BaseModel):
    tag_task_id: str = Field(None, title='任务id',
                             description='话题任务id')
    tag: str = Field(None, title='话题',
                     description='该话题内容')
    one_day: dict = Field(None, title='一天热度',
                          description='话题一天的热度数据')
    one_month: dict = Field(None, title='一月热度',
                            description='话题一个月内的热度数据')
    three_month: dict = Field(None, title='三月热度',
                              description='话题三个月内的热度数据')

