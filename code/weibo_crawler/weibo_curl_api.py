import tornado.ioloop
from tornado import web, gen, httpserver
import tornado.options
from tornado.options import define, options
import json

from selector_parser import *
import settings
from web_curl import SpiderAim, weibo_web_curl, curl_result_to_api_result
from weibo_curl_error import WeiboCurlError, CookieInvalidException, HTMLParseException
from account.account import account_pool
from utils import report_log
import pymongo


SEARCH_LIMIT_PAGES = 50  # 微博的搜索接口限制的最大页数


class BaseHandler(tornado.web.RequestHandler):
    def write(self, dict_data: dict):
        """在发送之前将编码方式转化成Unicode"""
        data = json.dumps(dict_data, ensure_ascii=False)
        super().write(data)

    def args2dict(self):
        """
        将请求url中的请求查询字符串转化成dict
        :return: 转化后的dict
        """
        input_dict = dict()
        args = self.request.arguments
        for i in args:
            input_dict[i] = self.get_argument(i)
        return input_dict

    def get_json(self):
        """
        将获取post时的json
        """
        json_str = self.request.body.decode('utf8')
        json_obj = json.loads(json_str)
        return json_obj

    def save_data_to_mongo(self, dict_data: list, table_name: str):
        """
        将获得的数据存到Mongo数据库中
        """
        mongo_client = pymongo.MongoClient('mongodb://localhost:27017')
        weibo_db = mongo_client['weibo']
        weibo_table = weibo_db[table_name]
        weibo_table.insert_many(dict_data)
        print('向Mongo写入数据成功')


class SearchTweetsHandler(BaseHandler):
    """
    微博搜索接口
        说明：根据关键词搜索微博
        路由：/weibo_curl/api/search_tweets
    """
    @gen.coroutine
    def get(self):
        # 获取参数
        args_dict = self.args2dict()   # 查询参数 -> 参数字典
        keyword, cursor, is_hot = args_dict.get('keyword'), args_dict.get(
            'cursor', '1'), args_dict.get('is_hot', False)
        if keyword is None:
            self.write(WeiboCurlError.REQUEST_LACK_ARGS)  # 缺少参数
            return
        try:
            cursor = 1 if not cursor else int(cursor)
        except ValueError:
            self.write(WeiboCurlError.REQUEST_ARGS_ERROR)
            return

        # 进行爬取
        search_weibo_curl_result = yield weibo_web_curl(SpiderAim.search_weibo,
                                                        keyword=keyword, page_num=cursor, is_hot=is_hot)
        if not search_weibo_curl_result['error_code']:
            self.response = search_weibo_curl_result['response']
        else:
            error_res = curl_result_to_api_result(search_weibo_curl_result)
            self.write(error_res)
            return
        # 构建解析器
        searchWeiboParser = SearchWeiboParser(self.response)
        # 获取微博信息
        try:
            weibo_list = searchWeiboParser.parse_page()
            # print(weibo_list)
        except HTMLParseException:
            self.write(WeiboCurlError.HTML_PARSE_ERROR)
            return

        if weibo_list is None:
            self.write(WeiboCurlError.PAGE_NOT_FOUND)  # 页面找不到
            return
        # 成功返回结果
        success = settings.SUCCESS.copy()
        success['data'] = {
            'result': weibo_list,
            'cursor': str(cursor + 1) if cursor < 50 else '0'
        }
        self.write(success)
        #self.save_data_to_mongo(weibo_list, 'search_tweets')
        print(success)
        return

    # @gen.coroutine
    # def get_all(self):
    #     """
    #     得到所有的50页信息
    #     """




class StatusesShowHandler(BaseHandler):
    """
    推文展示接口
    说明：根据推文id搜索推文
    路由：/weibo_curl/api/statuses_show
    """
    @gen.coroutine
    def get(self):
        # 获取参数
        args_dict = self.args2dict()
        weibo_id = args_dict.get('weibo_id')
        if weibo_id is None:
            self.write(WeiboCurlError.REQUEST_LACK_ARGS)
            return
        hot = args_dict.get('hot', False)  # 是否获取热评
        cursor = args_dict.get('cursor', '1')
        try:
            cursor = 1 if not cursor else int(cursor)
        except ValueError:
            self.write(WeiboCurlError.REQUEST_ARGS_ERROR)
            return
        if cursor > SEARCH_LIMIT_PAGES:
            results = settings.SUCCESS.copy()
            results['data'] = {
                'result': [],
                'cursor': '0'
            }
            self.write(results)
            return
        # 进行爬取
        comment_curl_result = yield weibo_web_curl(SpiderAim.weibo_comment, weibo_id=weibo_id, page_num=cursor)
        if not comment_curl_result['error_code']:
            self.response = comment_curl_result['response']
        else:
            error_res = curl_result_to_api_result(comment_curl_result)
            self.write(error_res)
            return
        # 构建解析器
        try:
            commonParser = CommentParser(weibo_id, response=self.response)
        except CookieInvalidException:
            self.write(WeiboCurlError.COOKIE_INVALID)
            return

        try:
            weibo_detail = yield commonParser.parse_one_weibo()
        except HTMLParseException as e:
            report_log(e)
            self.write(WeiboCurlError.HTML_PARSE_ERROR)
            return
        except Exception as e:
            report_log(e)
            self.write(WeiboCurlError.UNKNOWN_ERROR)
            return

        # 根据 hot 参数来确定获取 comment_list 的方式
        if not hot:
            comment_list = commonParser.get_all_comment()
        else:
            hot_comment_curl_result = yield weibo_web_curl(SpiderAim.hot_comment, weibo_id=weibo_id, page_num=cursor)
            if not hot_comment_curl_result['error_code']:
                self.hot_comment_response = hot_comment_curl_result['response']
            else:
                error_res = curl_result_to_api_result(comment_curl_result)
                self.write(error_res)
                return

            try:
                comment_list = HotCommentParser(
                    weibo_id, self.hot_comment_response).get_all_comment()
            except HTMLParseException:
                self.write(WeiboCurlError.HTML_PARSE_ERROR)
                return
            except Exception as e:
                report_log(
                    (__class__.__name__, StatusesShowHandler.get.__name__), e)
                self.write(WeiboCurlError.UNKNOWN_ERROR)
                return
        # 成功时返回结果
        weibo_detail['weibo_id'] = weibo_id
        weibo_detail['comments'] = comment_list
        success = settings.SUCCESS.copy()
        success['data'] = {
            'result': weibo_detail,
            'cursor': str(cursor + 1) if cursor < weibo_detail['max_page'] else '0'
        }
        print(success)
        self.write(success)
        return


class SearchUsersHandler(BaseHandler):
    """
    用户搜索接口
        说明：根据关键词搜索用户
        路由：/weibo_curl/api/users_search
    """
    @gen.coroutine
    def get(self):
        # 获取参数
        args_dict = self.args2dict()
        keyword, cursor = args_dict.get(
            'keyword'), args_dict.get('cursor', '1')
        if keyword is None:
            self.write(WeiboCurlError.REQUEST_LACK_ARGS)  # 缺少参数
            return
        try:
            cursor = 1 if not cursor else int(cursor)
        except ValueError:
            self.write(WeiboCurlError.REQUEST_ARGS_ERROR)
            return
        if cursor > SEARCH_LIMIT_PAGES:
            result = settings.SUCCESS.copy()
            result['data'] = {
                'result': [],
                'cursor': '0'
            }
            self.write(result)
            return
        user_type, gender, age_limit = args_dict.get(
            'user_type'), args_dict.get('gender'), args_dict.get('age_limit')
        # 进行爬取
        search_users_curl_result = yield weibo_web_curl(SpiderAim.search_users, keyword=keyword, user_type=user_type,
                                                        gender=gender, age_limit=age_limit, page_num=cursor)
        if not search_users_curl_result['error_code']:
            self.response = search_users_curl_result['response']
        else:
            error_res = curl_result_to_api_result(search_users_curl_result)
            self.write(error_res)
            return
        # 构建解析器
        searchUsersParser = SearchUsersParser(self.response)
        # 提取信息
        try:
            user_list = searchUsersParser.parse_page()
        except HTMLParseException:
            self.write(WeiboCurlError.HTML_PARSE_ERROR)
            return
        # 返回信息
        if user_list:
            # print(user_list)
            success = settings.SUCCESS.copy()
            success['data'] = {
                'result': user_list,
                'cursor': str(cursor + 1) if cursor < SEARCH_LIMIT_PAGES else '0'
            }
            self.write(success)
            return
        self.write(WeiboCurlError.UNKNOWN_ERROR)
        return


class UsersShowHandler(BaseHandler):
    """
    API: 用户展示接口：根据用户id搜索用户
    routing path: /weibo_curl/api/users_show
    """
    @gen.coroutine
    def get(self):
        args_dict = self.args2dict()
        user_id = args_dict.get('user_id')
        if user_id is None:  # 此时URL缺少查询参数
            self.write(WeiboCurlError.REQUEST_LACK_ARGS)
            return

        try:
            # 爬取主页的结果
            idx_curl_result = yield weibo_web_curl(SpiderAim.users_show, user_id=user_id)
            if not idx_curl_result['error_code']:
                idxParser = IndexParser(
                    user_id, idx_curl_result.get('response'))  # 构建一个主页解析器

                try:
                    user_id = idxParser.get_user_id()  # 获取到真正的user_id
                    max_page_num = idxParser.get_page_num()  # 获取微博的页数
                except CookieInvalidException:
                    self.write(WeiboCurlError.COOKIE_INVALID)
                    return

                # 爬取信息页的结果
                info_curl_result = yield weibo_web_curl(SpiderAim.users_info, user_id=user_id)
                if not info_curl_result['error_code']:
                    infoParser = InfoParser(
                        info_curl_result.get('response'))  # 信息页解析器
                    user_info = infoParser.extract_user_info()
                    user = idxParser.get_user(user_info)
                    user['max_page'] = max_page_num  # 微博的最大页数
                    # print(user)

                    success = settings.SUCCESS.copy()
                    try:
                        success['data'] = {
                            'result': user,
                            'cursor': ''
                        }
                    except AttributeError:  # user没有__dict__属性时，说明未爬取到user
                        self.write(WeiboCurlError.REQUEST_ARGS_ERROR)  # 报告参数错误
                        return
                    self.write(success)
                    return
                else:
                    error_res = curl_result_to_api_result(info_curl_result)
                    self.write(error_res)
                    return
            else:
                error_res = curl_result_to_api_result(idx_curl_result)
                self.write(error_res)
                return

        except HTMLParseException:
            self.write(WeiboCurlError.HTML_PARSE_ERROR)
            return
        except Exception as e:
            report_log(e)
            self.write(WeiboCurlError.UNKNOWN_ERROR)
            return


class UserTimelineHandler(BaseHandler):
    """
    API: 用户时间线接口
    根据用户id搜索用户的微博
    route: /weibo_curl/api/statuses_user_timeline
    """
    @gen.coroutine
    def get(self):
        args_dict = self.args2dict()
        user_id = args_dict.get('user_id')
        if user_id is None:  # 此时缺少参数
            self.write(WeiboCurlError.REQUEST_LACK_ARGS)
            return
        cursor = args_dict.get('cursor', '1')
        try:
            cursor = 1 if not cursor else int(cursor)
        except ValueError:
            self.write(WeiboCurlError.REQUEST_ARGS_ERROR)
            return
        filter = args_dict.get('filter', 0)  # 默认爬取全部微博（原创+转发）

        page_curl_result = yield weibo_web_curl(SpiderAim.users_weibo_page, user_id=user_id, page_num=cursor)
        if not page_curl_result['error_code']:
            pageParser = PageParser(
                user_id, page_curl_result['response'], filter)
        else:
            error_res = curl_result_to_api_result(page_curl_result)
            self.write(error_res)
            return

        try:
            weibos, max_page = yield pageParser.get_one_page()
            if cursor == 1:
                user = pageParser.get_user_info_when_first_page()
            else:
                user = pageParser.get_user_info_except_first_page()
        except HTMLParseException:
            self.write(WeiboCurlError.HTML_PARSE_ERROR)
            return
        success = settings.SUCCESS.copy()
        try:
            success['data'] = {
                'result': {
                    'user': user,
                    'weibos': [weibo.__dict__ for weibo in weibos]
                },
                'cursor': str(cursor + 1) if cursor < max_page else '0'
            }
        except AttributeError:  # user没有__dict__属性时，说明未爬取到user
            self.write(WeiboCurlError.REQUEST_ARGS_ERROR)  # 报告参数错误
            return
        # print(success)
        self.write(success)
        return


class FriendsHandler(BaseHandler):
    """
    用户朋友列表接口(朋友指关注的人)
        说明：根据用户id搜索用户朋友，同时也要返回他们的信息
        路由：/weibo_curl/api/friends_list
    """
    @gen.coroutine
    def get(self):
        # 获取查询参数
        args_dict = self.args2dict()
        user_id, cursor = args_dict.get(
            'user_id'), args_dict.get('cursor', '1')
        if user_id is None:
            self.write(WeiboCurlError.REQUEST_LACK_ARGS)
            return
        try:
            cursor = 1 if not cursor else int(cursor)
        except ValueError:
            self.write(WeiboCurlError.REQUEST_ARGS_ERROR)
            return
        # 进行爬取
        follow_curl_result = yield weibo_web_curl(SpiderAim.follow, user_id=user_id, page_num=cursor)
        if not follow_curl_result['error_code']:
            self.response = follow_curl_result['response']
        else:
            error_res = curl_result_to_api_result(follow_curl_result)
            self.write(error_res)
            return
        # 构建解析器
        followParser = FollowParser(self.response)
        # 提取相关信息并返回结果
        try:
            follow_list = followParser.get_follows()  # 关注者的列表
            max_page_num = followParser.get_max_page_num()  # 总页数
            if cursor < max_page_num:
                cursor = str(cursor + 1)
            success = settings.SUCCESS.copy()
            success['data'] = {
                'result': {
                    'friend_list': follow_list,
                    'max_page_num': max_page_num
                },
                'cursor': cursor
            }
            # print(success)
            self.write(success)
            return
        except HTMLParseException:
            self.write(WeiboCurlError.HTML_PARSE_ERROR)
            return
        except Exception as e:
            report_log(e)
            self.write(WeiboCurlError.UNKNOWN_ERROR)


class FollowersHandler(BaseHandler):
    """
    用户粉丝列表接口
        说明：根据用户id搜索用户粉丝
        路由：/weibo_curl/api/followers_list
    """
    @gen.coroutine
    def get(self):
        args_dict = self.args2dict()
        user_id, cursor = args_dict.get(
            'user_id'), args_dict.get('cursor', '1')
        if user_id is None:
            self.write(WeiboCurlError.REQUEST_LACK_ARGS)
            return
        try:
            cursor = 1 if cursor == 0 else int(cursor)
        except ValueError:  # 当对cursor转换产生错误时
            self.write(WeiboCurlError.REQUEST_ARGS_ERROR)
            return
        # 进行爬取
        fans_curl_result = yield weibo_web_curl(SpiderAim.fans, user_id=user_id, page_num=cursor)
        if not fans_curl_result['error_code']:
            self.response = fans_curl_result['response']
        else:
            error_res = curl_result_to_api_result(fans_curl_result)
            self.write(error_res)
            return
        # 构建解析器
        fansParser = FansParser(self.response)
        # 提取相关信息并返回结果
        try:
            fans_list = fansParser.get_fans()
            max_page_num = fansParser.get_max_page_num()
            if cursor < max_page_num:
                cursor = str(cursor + 1)
            success = settings.SUCCESS.copy()
            success['data'] = {
                'result': {
                    'follower_list': fans_list,
                    'max_page_num': max_page_num
                },
                'cursor': cursor
            }
            self.write(success)
            return

        except HTMLParseException:
            self.write(WeiboCurlError.HTML_PARSE_ERROR)
            return
        except Exception as e:
            report_log(e)
            self.write(WeiboCurlError.UNKNOWN_ERROR)


class AccountUpdateHandler(BaseHandler):
    """
    账号更新接口
        说明：接收一个包含有cookie和proxy的json文件并更新程序运行时向微博发送请求所携带的cookie与proxy
        路由：/weibo_curl/api/account
    """

    def post(self):
        json_obj = self.get_json()
        cookies, proxies = json_obj.get('cookies'), json_obj.get('proxies')

        try:
            account_pool.update(cookies, proxies)
        except ValueError:
            error = WeiboCurlError.REQUEST_ARGS_ERROR
            error['error_msg'] += 'Cookies or proxies is an empty list.'
            self.write(error)
            return

        success = settings.SUCCESS.copy()
        success['data'] = {
            'result': account_pool.accounts,
            'cursor': ''
        }
        self.write(success)
        return


# 启动主程序
if __name__ == '__main__':
    import platform

    if platform.system() == "Windows":
        import asyncio

        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    define(
        "port",
        default=settings.PORT_NUM,
        help="run on the given port",
        type=int)  # 定义端口号
    ROUTE_PREFIX = r"/weibo_curl/api/"  # 路由前缀

    app = tornado.web.Application([
        (ROUTE_PREFIX + r"users_show", UsersShowHandler),
        (ROUTE_PREFIX + r"statuses_user_timeline", UserTimelineHandler),
        (ROUTE_PREFIX + r"statuses_show", StatusesShowHandler),
        (ROUTE_PREFIX + r"friends_list", FriendsHandler),
        (ROUTE_PREFIX + r"followers_list", FollowersHandler),
        (ROUTE_PREFIX + r"search_tweets", SearchTweetsHandler),
        # (ROUTE_PREFIX + r"search_all_tweets", SearchTweetsHandler.get_all),
        (ROUTE_PREFIX + r"users_search", SearchUsersHandler),
        (ROUTE_PREFIX + r"account_update", AccountUpdateHandler)
    ])

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print('begin running...')
    tornado.ioloop.IOLoop.instance().start()
