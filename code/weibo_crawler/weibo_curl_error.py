class WeiboCurlError:
    """各种微博爬取过程的错误类型"""

    # 请求缺少参数
    REQUEST_LACK_ARGS = {
        'error_code': 2001,
        'error_msg': 'URL is lack of arguments.'
    }

    # 请求参数错误
    REQUEST_ARGS_ERROR = {
        'error_code': 2002,
        'error_msg': 'URL args error.'
    }

    # 登录失效
    LOGIN_ERROR = {
        'error_code': 2003,
        'error-msg': 'An error occurred while logging in.'
    }

    # 用户不存在
    PAGE_NOT_FOUND = {
        'error_code': 2004,
        'error_msg': "Can't find the page."
    }

    # 微博网站返回其他错误信息
    ABNORMAL_HTTP = {
        'error_code': 2005,
        'error_msg': "Sina weibo occur an abnormal http."
    }

    # 未知错误
    UNKNOWN_ERROR = {
        'error_code': 2006,
        'error_msg': "An unknown error has occurred here."
    }

    # Cookie失效
    COOKIE_INVALID = {
        'error_code': 2007,
        'error_msg': "Cookie invalid."
    }

    # ip失效
    IP_INVALID = {
        'error_code': 2008,
        'error_msg': 'Current ip address invalid.'
    }

    # HTML解析出错
    HTML_PARSE_ERROR = {
        'error_code': 2009,
        'error_msg': 'Error parsing HTML page.'
    }

    CONNECT_TIMED_OUT = {
        'error_code': 2010,
        'error_msg': 'Connection timed out.'
    }


class WeiboException(Exception):
    """微博爬虫项目的异常"""
    def __init__(self):
        super().__init__()



class CookieInvalidException(WeiboException):
    """Cookie失效的异常"""
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return 'Cookie invalid.'


class HTMLParseException(WeiboException):
    """HTML页面解析出错"""
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return "Error parsing HTML page."
