"""
: 人物分类dto
@author: lingzhi
@time: 2021/7/20 16:20
"""
from pydantic import Field, BaseModel
from enum import Enum


class Category(Enum):
    rumor = 0   # 推手
    faker = 1   # 水军
    user = 2    # 普通用户
    major = 3   # 最具影响力用户


class CharacterCategory(BaseModel):
    tag_task_id: str = Field(None, title='话题任务id', description='参照初始化任务时的任务id')
    tag_character_task_id: str = Field(None, title='人物角色分类id', description='依据节点特征对人物进行分类')
    user_id: str = Field(None, title='微博用户id')
    category: Category = Field(2, title='人物类别', description='暂分为推手（0）、水军（1）、普通用户（2）、最具影响力用户(3)')

