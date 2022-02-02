import logging

PORT_NUM = 8000  # app运行的端口号


# 发送一个request最多重新尝试的次数
RETRY_TIME = 3

# requests的headers
HEADERS = {
    "User-Agent": "MMozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52",
}
HEADERS_WITH_COOKIR = HEADERS.copy()
HEADERS_WITH_COOKIR["Cookie"] = ""

# requests的超时时长限制das
REQUEST_TIME_OUT = 10

# 爬取结果正确时返回结果的格式
SUCCESS = {
    'error_code': 0,
    'data': None,
    'error_msg': None
}

# 日志
LOGGING = logging
