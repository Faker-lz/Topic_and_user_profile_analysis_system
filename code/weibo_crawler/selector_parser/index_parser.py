from settings import LOGGING
from weibo_curl_error import CookieInvalidException, HTMLParseException
from .base_parser import BaseParser
import utils

class IndexParser(BaseParser):
    def __init__(self, user_id, response):
        super().__init__(response)
        self.user_id = user_id

    def get_user_id(self):
        """获取用户id，使用者输入的user_id不一定是正确的，可能是个性域名等，需要获取真正的user_id"""
        user_id = self.user_id
        url_list = self.selector.xpath("//div[@class='u']//a")
        for url in url_list:
            if (url.xpath('string(.)')) == u'资料':
                if url.xpath('@href') and url.xpath('@href')[0].endswith(
                        '/info'):
                    link = url.xpath('@href')[0]
                    user_id = link[1:-5]
                    break
        self.user_id = user_id
        return user_id

    def get_user(self, user_info):
        """获取用户信息、微博数、关注数、粉丝数"""
        self.user = user_info
        try:
            user_info = self.selector.xpath("//div[@class='tip2']/*/text()")
            self.user['id'] = self.user_id
            self.user['weibo_num'] = int(user_info[0][3:-1])
            self.user['following'] = int(user_info[1][3:-1])
            self.user['followers'] = int(user_info[2][3:-1])
            return self.user
        except Exception as e:
            utils.report_log(e)
            raise HTMLParseException

    def get_page_num(self):
        """获取微博总页数"""
        try:
            if not self.selector.xpath("//input[@name='mp']"):
                page_num = 1
            else:
                page_num = int(self.selector.xpath("//input[@name='mp']")
                               [0].attrib['value'])
            return page_num
        except Exception as e:
            utils.report_log(e)
            raise HTMLParseException

class InfoParser(BaseParser):
    def __init__(self, response):
        super().__init__(response)

    def extract_user_info(self):
        """提取用户信息"""
        user = USER_TEMPLATE.copy()
        nickname = self.selector.xpath('//title/text()')[0]
        nickname = nickname[:-3]
        # 检查cookie
        if nickname == u'登录 - 新' or nickname == u'新浪':
            LOGGING.warning(u'cookie错误或已过期')
            raise CookieInvalidException()

        user['nickname'] = nickname
        # 获取头像
        try:
            user['head'] = self.selector.xpath('//div[@class="c"]/img[@alt="头像"]')[0].get('src')
        except:
            user['head'] = ''
        # 获取基本信息
        try:
            basic_info = self.selector.xpath("//div[@class='c'][3]/text()")
            zh_list = [u'性别', u'地区', u'生日', u'简介', u'认证', u'达人']
            en_list = [
                'gender', 'location', 'birthday', 'description',
                'verified_reason', 'talent'
            ]
            for i in basic_info:
                if i.split(':', 1)[0] in zh_list:
                    user[en_list[zh_list.index(i.split(':', 1)[0])]] = i.split(':', 1)[1].replace('\u3000', '')


            if self.selector.xpath(
                    "//div[@class='tip'][2]/text()")[0] == u'学习经历':
                user['education'] = self.selector.xpath(
                    "//div[@class='c'][4]/text()")[0][1:].replace(
                    u'\xa0', u' ')
                if self.selector.xpath(
                        "//div[@class='tip'][3]/text()")[0] == u'工作经历':
                    user['work'] = self.selector.xpath(
                        "//div[@class='c'][5]/text()")[0][1:].replace(
                        u'\xa0', u' ')
            elif self.selector.xpath(
                    "//div[@class='tip'][2]/text()")[0] == u'工作经历':
                user['work'] = self.selector.xpath(
                    "//div[@class='c'][4]/text()")[0][1:].replace(
                    u'\xa0', u' ')
            return user
        except Exception as e:
            utils.report_log(e)
            raise HTMLParseException


# 封装一个用户信息的dict
USER_TEMPLATE = {
    'id': '',
    'nickname': '',
    'gender': '',
    'location': '',
    'birthday': '',
    'description': '',
    'verified_reason': '',
    'talent': '',
    'education': '',
    'work': '',
    'weibo_num': 0,
    'following': 0,
    'followers': 0
}