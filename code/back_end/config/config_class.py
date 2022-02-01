from pydantic import BaseSettings
from typing import Union, List, Dict, Any


class AppConfig(BaseSettings):
    """
    app启动的相关配置
    """
    HOST: str = '127.0.0.1'
    PORT: int = 81


class WeiBoConfig(BaseSettings):
    """weibo 爬虫api的相关配置"""
    BASEPATH: str = 'http://127.0.0.1:8000'
