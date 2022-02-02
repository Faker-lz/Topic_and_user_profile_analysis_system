import re

import utils
from .base_parser import BaseParser
from weibo_curl_error import HTMLParseException

class SearchUsersParser(BaseParser):
    """搜索用户页面的解析器"""

    USER_TEMPLATE = {
        'user_id': None,  # 用户的id
        'nickname': None,  # 昵称
        'head': None,
        'title': None,  # 所拥有的头衔
        'verified_reason': None,  # 认证原因
        'gender': None,  # 性别
        'location': None,  # 位置
        'description': None,  # 简介
        'tags': None,  # 标签
        'education': None,  # 教育信息
        'work': None,  # 工作信息
        'weibo_num': None,  # 微博数
        'following': None,  # 关注数
        'followers': None  # 粉丝数
    }

    @staticmethod
    def make_a_user():
        """生成一个用来存储一个user信息的dict"""
        return SearchUsersParser.USER_TEMPLATE.copy()

    def __init__(self, response):
        super().__init__(response)


    def parse_page(self):
        """解析网页"""
        try:
            user_list = self._get_all_user()
            return user_list
        except Exception as e:
            utils.report_log(e)
            raise HTMLParseException


    def _get_all_user(self):
        """获取全部用户信息"""
        user_list = list()
        user_nodes = self.selector.xpath('//div[@id="pl_user_feedList"]/div')
        for node in user_nodes:
            user = self._parse_one_user(node)
            # print(user)
            user_list.append(user)
        return user_list




    def _parse_one_user(self, user_node):
        """解析单个用户的selector节点"""
        user = SearchUsersParser.make_a_user()
        # 获取用户头像
        try:
            user['head'] = user_node.xpath('.//div[@class="avator"]/a/img')[0].get('src')
        except:
            user['head'] = ''
        # 获取其他信息
        info_selector = user_node.xpath('./div[@class="info"]')[0]
        headers = info_selector.xpath('./div[1]/a')

        if len(headers) > 2:  # 拥有头衔的情况
            header_node = headers[1]
            title = header_node.get('title')
            if title is not None:
                user['title'] = title


        user_id = headers[-1].get('uid')
        if user_id is None:
            # 尝试另外一种方法获取uid
            user_index_url = headers[0].get('href')
            pattern1 = re.compile(r'(?<=com/u/).+')  # 正则匹配 '//weibo.com/u/61248565' 类型，提取出其中的'61248565'
            user_id = pattern1.search(user_index_url)
            if user_id is not None:
                user_id = user_id.group()
            else:
                # 尝试另外一种方法获取uid
                pattern2 = re.compile(r'(?<=com/).+')  # 正则匹配 'weibo.com/xiena' 类型，提取出其中的'xiena'
                user_id = pattern2.search(user_index_url)
                if user_id is not None:
                    user_id = user_id.group()
        user['user_id'] = user_id

        user['nickname'] = ''.join(headers[0].xpath(".//text()"))

        all_p_node = info_selector.xpath('./p')
        first_p = all_p_node[0]
        gender_info = first_p.xpath('./i')[0].get('class')
        user['gender'] = 0 if gender_info.rfind('female') != -1 else 1  # 0为女性，1位男性
        user['location'] = ''.join(first_p.xpath('./text()')).strip()

        footer = None
        other_p_nodes = list()
        for p_node in all_p_node:
            if p_node is first_p:
                continue
            elif len(p_node.xpath('./span')) == 3:
                footer = p_node
            else:
                other_p_nodes.append(p_node)

        if footer is not None:
            spans = footer.xpath('./span')
            user['following'] = spans[0].xpath('./a/text()')[0]
            user['followers'] = spans[1].xpath('./a/text()')[0]
            user['weibo_num'] = spans[2].xpath('./a/text()')[0]

        for node in other_p_nodes:
            info = ''.join(node.xpath('.//text()'))
            info_type = info[0: 2]

            if info_type == '教育':
                user['education'] = info
            elif info_type == '职业':
                user['work'] = info
            elif info_type == '简介':
                user['description'] = info
            elif info_type == '标签':
                user['tags'] = node.xpath('./a/text()')
            else:
                user['verified_reason'] = info

        return user



