"""
: tag基本数据结构
@author: lingzhi
@time: 2021/7/20 17:07
"""
from pydantic import BaseModel, Field


class User(BaseModel):
    """
    重要用户信息
    """
    user_id: str = Field(None, title='用户的id')
    head: str = Field(None, title='头像url')
    nickname: str = Field(None, title='用户名')
    birthday: str = Field(None, title='生日')
    verified_reason: str = Field(None, title='认证信息')
    gender: str = Field(None, title='性别')
    location: str = Field(None, title='位置')
    description: str = Field(None, title='简介')
    education: str = Field(None, title='受教育信息')
    work: str = Field(None, title='工作信息')
    weibo_num: str = Field(None, title='微博数')
    following: str = Field(None, title='关注数')
    followers: str = Field(None, title='粉丝数')
    max_page: int = Field(None, title='个人微博的最大页数')


class ProgressTask(BaseModel):
    """
    执行中的任务
    """
    tag_task_id: str = Field(None, title='话题任务id')
    tag: str = Field(None, title='话题名称', description='用户输入的查询话题')
    status: str = Field(None, title='任务状态', description='后端实时任务状态')


class TagBase(BaseModel):
    """
    话题的基本信息
    """
    tag_task_id: str = Field(None, title='话题任务id')
    tag: str = Field(None, title='话题名称', description='用户输入的查询话题')
    user_count: int = Field(None, title='涉及用户数量', description='话题涉及用户数量')
    weibo_count: int = Field(None, title='涉及博文数量', description='话题涉及博文数量')
    vital_user: User = Field(None, title='最具影响力用户基本信息',
                            description='dict(用户名、头像url、昵称、认证、标签、粉丝数)')



