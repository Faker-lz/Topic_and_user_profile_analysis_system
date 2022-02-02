from tornado import gen
from tornado.curl_httpclient import CurlError
from tornado.httpclient import AsyncHTTPClient, HTTPError
from enum import Enum, unique
import re

import settings
import request_builder
from weibo_curl_error import WeiboCurlError


@unique  # 确保枚举值唯一
class SpiderAim(Enum):
    """枚举全部爬取目标，每个目标的value为对应的RequestBuilder"""
    users_show = request_builder.UserIndexReqBuilder
    users_info = request_builder.UserInfoReqBuilder
    users_weibo_page = request_builder.UserWeiboPageReqBuilder
    weibo_comment = request_builder.WeiboCommentReqBuilder
    hot_comment = request_builder.HotCommentReqBuilder
    mblog_pic_all = request_builder.MblogPicAllReqBuilder
    follow = request_builder.FollowsReqBuilder
    fans = request_builder.FansReqBuilder
    search_weibo = request_builder.SearchWeiboReqBuilder
    search_users = request_builder.SearchUsersReqBuilder


# AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

@gen.coroutine
def weibo_web_curl(curl_aim: SpiderAim,
                   retry_time=settings.RETRY_TIME, with_cookie=True, **kwargs):
    """
    根据爬取的目标对相对应的网站发送request请求并获得response
    :param curl_aim: 爬取的目标，其值必须为Aim枚举值
    :param retry_time: 最多尝试发送request的次数
    :param kwargs: 需要转发给RequestBuilder的初始化参数
    :return: 当参数use_bs4为True时返回bs4解析的soup，False时返回etree解析后的selector
    """
    global response
    client = AsyncHTTPClient()
    # 将 curl_aim 转换成 RequestBuilder 类
    RequestBuilder = curl_aim.value
    # 构建请求并发送
    for epoch in range(retry_time):  # 最多进行retry_time次的请求尝试
        request = RequestBuilder(
            **kwargs).make_request(with_cookie=with_cookie)  # 获得 http request

        try:
            response = yield client.fetch(request)  # 发出请求获取响应
            # print(response.body)

            # 检查是否Cookie失效
            try:
                charset_pattern = re.compile(r'(?<=charset=").+(?=")')
                charset = charset_pattern.search(response.body.decode(
                    'ascii', errors='ignore')).group()  # 获取该网页的编码方案
                # print(response.body.decode(charset))
                # 用于寻找html中title部分的正则匹配pattern
                title_pattern = re.compile(r'<title>.*</title>')
                html_title = title_pattern.search(
                    response.body.decode(charset)).group(0)
                if html_title == '<title>新浪通行证</title>' or html_title == '<title>登录 - 新浪微博</title>':
                    settings.LOGGING.error(
                        'Cookie错误或失效! 失效Cookie为{}'.format(
                            request.headers.get('Cookie')))
                    return {'error_code': 3, 'errmsg': 'Invalid cookie: {}'.format(
                        request.headers.get('Cookie'))}
            except (UnicodeDecodeError, AttributeError):
                pass
        except CurlError as e:  # 连接超时
            if epoch < settings.RETRY_TIME:
                continue
            return {'error_code': 5, 'errmsg': str(e)}
        except HTTPError as e:  # 其他HTTP错误
            if epoch < settings.RETRY_TIME:
                continue
            return {'error_code': 1, 'errmsg': str(e)}

        # 根据 http code 返回对应的信息
        http_code = response.code
        if http_code == 200:
            return {'error_code': 0, 'response': response}
        # 非200时进行重试
        if epoch < settings.RETRY_TIME:
            continue
        # 若重试多次仍然错误，就返回报错
        if http_code == 302 or http_code == 403:  # Cookie 失效
            return {'error_code': 3, 'errmsg': 'Invalid cookie: {}'.format(
                request.headers.get('Cookie'))}
        elif http_code == 418:  # ip失效，偶尔产生，需要再次请求
            return {'error_code': 4,
                    'errmsg': 'Please change a proxy and send a request again'}
        else:
            return {'error_code': 1,
                    'errmsg': 'Http status code: {}'.format(http_code)}

    return {'error_code': 5, 'errmsg': ''}


def curl_result_to_api_result(curl_result):
    """
    将 weibo_web_curl 返回的错误结果进行处理获得对应的错误信息
    """
    error_code = curl_result.get('error_code')
    # 将 error_code 转化为 WeiboCurlError 中的错误信息结果
    code_to_res = {
        1: lambda: WeiboCurlError.ABNORMAL_HTTP.copy(),
        2: lambda: WeiboCurlError.REQUEST_ARGS_ERROR.copy(),
        3: lambda: WeiboCurlError.COOKIE_INVALID.copy(),
        4: lambda: WeiboCurlError.IP_INVALID.copy(),
        5: lambda: WeiboCurlError.CONNECT_TIMED_OUT.copy()
    }

    error_res = code_to_res.get(error_code)()
    if error_res is not None:
        error_res['error_msg'] += curl_result.get('errmsg')
    else:
        error_res = WeiboCurlError.UNKNOWN_ERROR.copy()
    return error_res
