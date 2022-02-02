import settings
from tornado.httpclient import HTTPRequest
import enum
from account.account import account_pool


class BaseRequestBuilder:
    """用以根据参数构造出request的相关信息"""

    def __init__(self):
        self.url = str()

    def get_url(self):
        return self.url

    def make_request(self, method='GET', with_cookie=True, **req_kwargs):
        cookie, proxy = account_pool.fetch()
        proxy_host, proxy_port = proxy[0], proxy[1]

        if with_cookie:
            headers = settings.HEADERS_WITH_COOKIR
            headers['Cookie'] = cookie
        else:
            headers = settings.HEADERS

        # print(proxy_host, proxy_port)
        req = HTTPRequest(url=self.get_url(), method=method,
                          # proxy_host=proxy_host, proxy_port=proxy_port,
                          # connect_timeout=300, validate_cert=False,
                          headers=headers,
                          request_timeout=settings.REQUEST_TIME_OUT, **req_kwargs)
        return req


class UserIndexReqBuilder(BaseRequestBuilder):
    """根据用户id构造出用户的主页URL"""

    def __init__(self, user_id='1669879400'):
        super().__init__()
        self.url = 'https://weibo.cn/{}'.format(user_id)


class UserInfoReqBuilder(BaseRequestBuilder):
    """根据用户id构造出用户的信息页URL"""

    def __init__(self, user_id):
        super().__init__()
        self.url = 'https://weibo.cn/{}/info'.format(user_id)


class UserWeiboPageReqBuilder(BaseRequestBuilder):
    """根据用户id构造用户的某一页微博的URL"""

    def __init__(self, user_id, page_num=1):
        super().__init__()
        self.url = 'https://weibo.cn/{}?page={}'.format(user_id, page_num)


class WeiboCommentReqBuilder(BaseRequestBuilder):
    """根据weibo_id获取该微博的评论URL"""

    def __init__(self, weibo_id, page_num=1):
        super().__init__()
        self.url = 'https://weibo.cn/comment/{}?page={}'.format(
            weibo_id, page_num)


class HotCommentReqBuilder(BaseRequestBuilder):
    """根据weibo_id获取该微博的热门评论的URL"""

    def __init__(self, weibo_id, page_num=1):
        super().__init__()
        self.url = 'https://weibo.cn/comment/hot/{}?page={}'.format(
            weibo_id, page_num)


class MblogPicAllReqBuilder(BaseRequestBuilder):
    """微博所有图片的URL"""

    def __init__(self, weibo_id):
        super().__init__()
        self.url = 'https://weibo.cn/mblog/picAll/' + weibo_id + '?rl=1'


class FollowsReqBuilder(BaseRequestBuilder):
    """一个用户关注的人的URL"""

    def __init__(self, user_id, page_num):
        super().__init__()
        self.url = 'https://weibo.cn/{}/follow?page={}'.format(
            user_id, page_num)


class FansReqBuilder(BaseRequestBuilder):
    """一个用户的粉丝页的URL"""

    def __init__(self, user_id, page_num):
        super().__init__()
        self.url = 'https://weibo.cn/{}/fans?page={}'.format(user_id, page_num)


class SearchWeiboReqBuilder(BaseRequestBuilder):
    """用于搜索微博的页面URL"""

    def __init__(self, keyword, page_num, is_hot):
        super().__init__()
        search_type = r"xsort=hot&suball=1&Refer=g" if is_hot else r"typeall=1&suball=1"
        self.url = 'https://s.weibo.com/weibo?{}&page={}&q={}'.format(
            search_type, page_num, keyword)


class UserType(enum.Enum):
    """搜索用户时的用户类型限制"""
    NO_LIMIT = ''  # 无限制
    ORG_VIP = '&auth=org_vip'  # 机构认证
    PER_VIP = '&auth=per_vip'  # 个人认证
    ORDINARY = '&auth=ord'  # 普通用户

    @staticmethod
    def arg_convert(arg):
        return {
            None: UserType.NO_LIMIT,
            1: UserType.ORG_VIP,
            2: UserType.PER_VIP,
            3: UserType.ORDINARY
        }.get(arg, UserType.NO_LIMIT)


class Gender(enum.Enum):
    """搜索用户时的性别限制"""
    NO_LIMIT = ''
    MAN = '&gender=man'
    WOMAN = '&gender=woman'

    @staticmethod
    def arg_convert(arg):
        return {
            None: Gender.NO_LIMIT,
            1: Gender.MAN,
            2: Gender.WOMAN
        }.get(arg, Gender.NO_LIMIT)


class AgeLimit(enum.Enum):
    """枚举搜索用户时的年龄限制"""
    NO_LIMIT = ''  # 不限年龄
    BELOW_18 = '&age=18y'  # 18岁以下
    FROM_19_TO_22 = '&age=22y'  # 19-22岁
    FROM_23_TO_29 = '&age=29y'  # 23-29岁
    FROM_30_TO_39 = '&age=39y'  # 30-39岁
    OVER_40 = '&age=40y'  # 高于40岁

    @staticmethod
    def arg_convert(arg):
        return {
            None: AgeLimit.NO_LIMIT,
            1: AgeLimit.BELOW_18,
            2: AgeLimit.FROM_19_TO_22,
            3: AgeLimit.FROM_30_TO_39,
            4: AgeLimit.OVER_40
        }.get(arg, AgeLimit.NO_LIMIT)


class SearchUsersReqBuilder(BaseRequestBuilder):
    """用于搜索用户的页面URL"""

    def __init__(self, keyword, user_type, gender, age_limit, page_num):
        """
        :param keyword: 搜索关键字
        :param user_type: 用户类型
        :param gender: 性别
        :param age_limit: 年龄限制
        :param page_num: 页数
        """
        super().__init__()
        # 先将这些参数转化成对应枚举类型
        user_type = UserType.arg_convert(user_type)
        gender = Gender.arg_convert(gender)
        age_limit = AgeLimit.arg_convert(age_limit)
        # 再将这些枚举类型转化成url的查询字符串
        query_str = ''.join((user_type.value, gender.value, age_limit.value))

        self.url = 'https://s.weibo.com/user?q={}&Refer=weibo_user{}&page={}'.format(
            keyword, query_str, page_num)


if __name__ == '__main__':
    from tornado import httpclient

    def f():
        http_client = httpclient.HTTPClient()
        try:
            req = UserIndexReqBuilder('1669879400').make_request()
            response = http_client.fetch(req)
            print(response.body.decode('utf8'))
        except Exception as e:
            print(e)

    f()
