"""
: 
@author: lingzhi
@time: 2021/7/19 17:20
"""

from fastapi import FastAPI
from controller import api_router
import exception_handlers


# 生成的API文档中的tag元信息
tags_metadata = [
    {
        'name': 'test',
        'description': '用于测试程序的接口'
    },
]


main_app = FastAPI(
    title='Yuqing Analyse System',
    description='舆情分析系统',
    version='0.0.1',
    openapi_tags=tags_metadata
)

# include api router
main_app.include_router(api_router, prefix='/api')

# 为 app 注册异常处理器
exception_handlers.register_exception_handler(main_app)


