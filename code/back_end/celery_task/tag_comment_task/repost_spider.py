"""
@version: v0.1
@description：爬微博转发
"""
import requests
import re
import datetime
import random
import logging
from lxml import etree
from celery_task import celeryapp
import time

from celery_task.config import mongo_conf
from celery_task.utils import mongo_client

logger = logging.getLogger()

PAGE_SIZE = 100

BASE_DOMAIN = 'https://weibo.cn'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
    'Cookie': 'SCF=ArHSivJ7DBzxAALySACWrOzWulmqj_Zr5aggjL8afVQ6Pv6H5lPXm0_tiSktPqlqBSw2OfeX6twDrveJcbYNzs8.; SUB=_2A25Me5PlDeRhGeNJ61AY9irNyjSIHXVvhz2trDV6PUJbktAKLVfgkW1NSBz5nlaR7-8he36k3F4M3RxKcvLIEQUn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5zGJz1gR-_JrXo1iQ6.RlL5NHD95QfS05E1KqXeK2RWs4Dqcjgi--ciK.4i-iWi--4iKLFi-zcCcLV97tt; SSOLoginState=1635771317; _T_WM=86561739983; WEIBOCN_FROM=1110006030; MLOGIN=1; XSRF-TOKEN=c6f982; M_WEIBOCN_PARAMS=oid=4698660040084390&luicode=20000174&uicode=20000174'
}

keyword_re = re.compile('<span class="kt">|</span>|原图|<!-- 是否进行翻译 -->|<span class="cmt">|\[组图共.+张\]')
emoji_re = re.compile('<img alt="|" src="//h5\.sinaimg(.*?)/>')
white_space_re = re.compile('<br />')
div_re = re.compile('</div>|<div>')
image_re = re.compile('<img(.*?)/>')
url_re = re.compile('<a href=(.*?)>|</a>')


def extract_repost_content(repost_html):
    s = repost_html
    if 'class="cc">' in s:
        s = s.split('<span class="cc">', maxsplit=1)[0]
    s = emoji_re.sub('', s)
    s = keyword_re.sub('', s)
    s = url_re.sub('', s)
    s = div_re.sub('', s)
    s = image_re.sub('', s)
    s = white_space_re.sub(' ', s)
    s = s.replace('\xa0', '')
    s = s.replace('<div class="c">', '')
    s = s.strip(':')
    s = s.strip()
    return s


def time_fix(time_string):
    now_time = datetime.datetime.now()
    if '分钟前' in time_string:
        minutes = re.search(r'^(\d+)分钟', time_string).group(1)
        created_at = now_time - datetime.timedelta(minutes=int(minutes))
        return created_at.strftime('%Y-%m-%d %H:%M')

    if '小时前' in time_string:
        minutes = re.search(r'^(\d+)小时', time_string).group(1)
        created_at = now_time - datetime.timedelta(hours=int(minutes))
        return created_at.strftime('%Y-%m-%d %H:%M')

    if '今天' in time_string:
        return time_string.replace('今天', now_time.strftime('%Y-%m-%d'))

    if '月' in time_string:
        time_string = time_string.replace('月', '-').replace('日', '')
        time_string = str(now_time.year) + '-' + time_string
        return time_string

    return time_string


def name2uid(name_url):
    """
    将转化/n url 为/u url  通过用户名获取用户id
    :param name_url:用户名形式的url 例如：/n/%E5%B7%AB%E5%B1%B1%E5%85%AD%E6%9C%88%E9%9B%AA
	:return: uid 例如：6010658056
    """

    uid_re = re.compile("uid=(\d+)")
    time.sleep(1)
    response = requests.get("{domain}{name_url}".format(domain=BASE_DOMAIN, name_url=name_url),
                            headers=HEADERS)
    uid = re.findall(uid_re, response.url)[0]
    if uid:
        return uid
    else:
        # todo 需要处理可能的cookie失效和网络问题
        return 0000


def get_repost_list(repo_node, pre_content):
    """
    将一条转发拆解为转发节点列表
    :param repo_node:
    :param pre_content:
    :return:
    """
    # url_res = re.compile('<a href=\"(.*?)\">(.*?)</a>.*?\:(.*?)//')
    url_res = re.compile('<a href=\"(.*?)\">(.*?)</a>')
    repo_content_str = etree.tostring(repo_node, encoding='unicode').split('<span class="cc">', 1)[0]
    uid_list = re.findall(url_res, repo_content_str)
    # print(repost_item)
    content_split_list = pre_content.split("//@")
    repost_list = []
    for i in range(1, len(content_split_list)):
        repost_dict = dict()
        repost_dict["user_name"] = content_split_list[i].split(":", maxsplit=1)[0]
        repost_dict["content"] = content_split_list[i].split(":", maxsplit=1)[1]
        repost_dict["page_url"] = uid_list[i][0]
        # repost_dict["uid"] = name2uid(uid_list[i][0])
        repost_list.append(repost_dict)
    return repost_list


def spider(tag_task_id: str, weibo_id='K7okwxcKa', page=93, tag_comment_task_id=9999):
    """
    爬取微博评论函数
    :param tag_task_id: 话题任务id
    :param tag_comment_task_id: 评论任务id
    :param weibo_id:微博id
    :param page: 起始页数
    :param task_id: 任务id
    :return:
    """
    response = requests.get(
        "{domain}/repost/{weibo_id}?page={page}".format(domain=BASE_DOMAIN, weibo_id=weibo_id, page=page),
        headers=HEADERS)
    # response = requests.get(
    #     "{domain}/repost/{weibo_id}?page={page}".format(domain=BASE_DOMAIN, weibo_id=weibo_id, page=page),
    #     headers=HEADERS)
    tree_node = etree.HTML(response.text.encode('utf-8'))
    repo_nodes = tree_node.xpath('//div[@class="c" and not(contains(@id,"M_"))]')
    repost_items = []
    for repo_node in repo_nodes:
        try:
            if repo_node:
                repo_user_url = repo_node.xpath('.//a[contains(@href,"/u/")]/@href')
                if not repo_user_url:
                    continue
                repost_item = {}
                repost_item["tag_comment_task_id"] = tag_comment_task_id
                repost_item["tag_task_id"] = tag_task_id
                repost_item['crawl_time'] = int(time.time())
                repost_item['weibo_id'] = response.url.split('/')[-1].split('?')[0]
                repost_item['page'] = page
                repost_item['user_id'] = re.search(r'/u/(\d+)', repo_user_url[0]).group(1)
                repost_item['user_name'] = repo_node.xpath('.//a[contains(@href,"/u/")]/text()')[0].strip()
                content = extract_repost_content(etree.tostring(repo_node, encoding='unicode'))
                repost_item['pre_content'] = content.split(':', maxsplit=1)[1].strip()
                for content_item in repost_item['pre_content'].split(':'):
                    if '//@' not in content_item and '回复@' not in content_item:
                        repost_item['content'] = content_item if content_item.rfind('<') <0 else content_item[0: content_item.rfind('<')]
                        break
                repost_item['content'] = '' if '@' in repost_item['content'] else repost_item['content']
                created_at_info = repo_node.xpath('.//span[@class="ct"]/text()')[0].split('\xa0')
                repost_item['created_at'] = time_fix((created_at_info[0] + created_at_info[1]))
                repost_item["repost"] = get_repost_list(repo_node, repost_item['pre_content'])
                print(repost_item['content'])
                repost_items.append(repost_item)
        except Exception as e:
            # 可能会匹配到某些xpath节点，有些是无用数据，有些目前模板无法处理
            with open("./log/untreated.log", "a+", encoding="utf-8") as f:
                f.write(etree.tostring(repo_node, encoding='unicode'))
                f.write("\n")
            raise e
    if len(repost_items) == 0:
        # 请求下来的页面可能没有转发
        # with open("./log/page.log", "a+", encoding="utf-8") as f:
        #     f.write(response.text)
        #     f.write("\n")
        pass
    return repost_items


# todo 从当前节点开始而不是从根节点开始；若从根节点开始可能有重复爬取与分析的可能
@celeryapp.task(bind=True)
def spider_list(self, tag_task_id: str, weibo_id='K7okwxcKa', tag_comment_task_id=9999):
    response = requests.get("{domain}/repost/{weibo_id}?page=1".format(domain=BASE_DOMAIN, weibo_id=weibo_id),
                            headers=HEADERS)
    all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
    if all_page:
        all_page = all_page.group(1)
        all_page = int(all_page)
        if all_page > 300:
            all_page = 300 + all_page//300
    else:
        all_page = 10
    page_data = list()
    for page_num in range(1, all_page + 1):
        print(f'{page_num}/{all_page}')
        time.sleep(random.uniform(1, 10))
        try:
            result = spider(tag_task_id=tag_task_id, weibo_id=weibo_id, page=page_num,
                       tag_comment_task_id=tag_comment_task_id)
            if result:
                page_data.extend(result)
            if page_num % 10 == 0 or page_num == all_page:
                mongo_client.db[mongo_conf.COMMENT_REPOSTS].insert_many(page_data)
                page_data.clear()
                print('save')
            self.update_state(state='PROGRESS',
                              meta={'current': page_num, 'total': all_page,
                                    'task': weibo_id, 'task_id': tag_comment_task_id})
        except TypeError as e:
            logger.error("spider task error weibo_id {} task_id {} TypeError {}"
                         .format(weibo_id, tag_comment_task_id, str(e)))
        except Exception as e:
            logger.error("spider task error weibo_id {} task_id {} error {}"
                         .format(weibo_id, tag_comment_task_id, str(e)))
            continue


def spider_list_part(tag_task_id: str, weibo_id='K7okwxcKa', tag_comment_task_id=9999):
    print(weibo_id)
    response = requests.get("{domain}/repost/{weibo_id}?page=1".format(domain=BASE_DOMAIN, weibo_id=weibo_id),
                            headers=HEADERS)
    all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
    reports = list()
    if all_page:
        all_page = all_page.group(1)
        all_page = int(all_page)
    else:
        all_page = 10
    print(all_page)
    for page_num in range(1, all_page + 1):
        time.sleep(0.5)
        try:
            time.sleep(1)
            reports.append(spider(tag_task_id=tag_task_id, weibo_id=weibo_id, page=page_num,
                                  tag_comment_task_id=tag_comment_task_id))
            # with Mongo(mongo_conf.COMMENT_REPOSTS, mongo_conf.DB_NAME) as mydb:
            #     mydb.collect.insert_many(spider(tag_task_id=tag_task_id, weibo_id=weibo_id, page=page_num,
            #                              tag_comment_task_id=tag_comment_task_id))
        except TypeError:
            continue
        except Exception as e:
            logger.error("spider task error weibo_id {} task_id {} error {}"
                         .format(weibo_id, tag_comment_task_id, str(e)))
            continue
    for report in reports:
        mongo_client.db[mongo_conf.COMMENT_REPOSTS].insert_many(report)


if __name__ == '__main__':
    spider_list(tag_task_id='111', weibo_id='JlQ98A4K7')
    # spider(tag_task_id='11',weibo_id='JlQ98A4K7')