"""
: api启动文件
@author: lingzhi
@time: 2021/7/19 17:21
"""
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

import app
from config import app_conf

if __name__ == '__main__':
    # 前端页面url
    origins = [
        "*"
    ]

    # 后台api允许跨域
    app.main_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(app.main_app,
                host=app_conf.HOST,
                port=app_conf.PORT,)

