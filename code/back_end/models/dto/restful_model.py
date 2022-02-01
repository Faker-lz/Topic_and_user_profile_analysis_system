"""
: 
@author: lingzhi
@time: 2021/7/19 19:55
"""
from pydantic import Field
from pydantic.generics import GenericModel
from typing import Generic, TypeVar, Optional


T = TypeVar('T')  # 泛型类型 T


class RESTfulModel(GenericModel, Generic[T]):
    """
    RESTful 风格的数据模型，所有 response 统一采用改模型

    Examples
    --------
    >>> from fastapi import FastAPI
    >>> from typing import Dict
    >>> app = FastAPI()
    >>>
    >>> @app.get('/test/', response_model=RESTfulModel[Dict])
    >>> def view_func():
    >>>     ...
    """
    code: int = Field(default=0, title='错误码', description='正常状态下返回0')
    data: Optional[T] = Field(default=None, title='响应的数据部分')