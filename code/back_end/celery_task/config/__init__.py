"""
:task相关配置
@author: lingzhi
* @date 2021/8/12 20:27
"""
from .obj import (
    mongo_conf,
    celery_conf,
    es_conf
)
import logging
from jsonformatter import JsonFormatter

# 日志
LOGGING = logging.getLogger()
# LOGGING.setLevel(logging.INFO)
LOGGING.setLevel(70)
STRING_FORMAT = '''{
    "levelname": "levelname",
    "process": "process",
    "filename": "filename", 
    "funcName": "funcName",
    "lineno": "lineno", 
    "time": "asctime",
    "message": "message"
}'''
formatter = JsonFormatter(STRING_FORMAT, ensure_ascii=False, mix_extra=True)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
sh.setLevel(logging.DEBUG)
LOGGING.addHandler(sh)

#APM
APM_URL = 'http://127.0.0.1:8200'
APM = None
