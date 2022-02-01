"""
: 
@author: lingzhi
@time: 2021/7/20 17:13
"""
from pydantic import BaseModel, Field
from typing import List


class WordCloud(BaseModel):
    tag_task_id: str = Field(None, title='话题任务id')
    tag_word_cloud_task_id: str = Field(None, title='词云的id')
    data: List[dict] = Field(None, title='数据内容',
                             description='每一个元素都是key，value组成，key表示聚类后的关键字，value表示出现过的次数')
