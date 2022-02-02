import re
from urllib.parse import unquote

import utils
from weibo_curl_error import CookieInvalidException, HTMLParseException
from .base_parser import BaseParser


class SearchWeiboParser(BaseParser):
    def __init__(self, response):
        super().__init__(response)

    def parse_page(self):
        """
        解析网页
        """
        # 检查页面是否为空
        check_empty = self.selector.xpath('//div[@class="card card-no-result s-pt20b40"]')
        if len(check_empty) != 0:
            return None
        try:
            weibo_list = self._get_all_weibo()
            return weibo_list
        except Exception as e:
            utils.report_log(e)
            raise HTMLParseException

    def _get_all_weibo(self):
        """
        获取全部微博
        """
        weibo_list = list()
        for weibo in self._parse_weibo():
            if weibo is not None:
                weibo_list.append(weibo)
        return weibo_list

    def _parse_weibo(self):
        """解析网页中的微博信息"""
        selector = self.selector
        for sel in selector.xpath("//div[@class='card-wrap']"):
            info = sel.xpath(
                "div[@class='card']/div[@class='card-feed']/div[@class='content']/div[@class='info']"
            )
            if len(info) != 0:
                weibo = dict()
                # weibo['id'] = sel.xpath('@mid')[0]

                # 获取头像
                try:
                    weibo['head'] = sel.xpath('.//div[@class="avator"]/a//img')[0].get('src')
                except:
                    weibo['head'] = ''

                weibo['weibo_id'] = sel.xpath('(.//p[@class="from"])[last()]/a[1]/@href')[0].split('/')[-1].split('?')[0]
                weibo['user_id'] = info[0].xpath(
                    'div[2]/a/@href')[0].split('?')[0].split('/')[-1]
                weibo['screen_name'] = info[0].xpath(
                    'div[2]/a/@nick-name')[0]
                txt_sel = sel.xpath('.//p[@class="txt"]')[0]
                retweet_sel = sel.xpath('.//div[@class="card-comment"]')
                retweet_txt_sel = ''
                if retweet_sel and retweet_sel[0].xpath('.//p[@class="txt"]'):
                    retweet_txt_sel = retweet_sel[0].xpath(
                        './/p[@class="txt"]')[0]
                content_full = sel.xpath(
                    './/p[@node-type="feed_list_content_full"]')
                is_long_weibo = False
                is_long_retweet = False
                if content_full:
                    if not retweet_sel:
                        txt_sel = content_full[0]
                        is_long_weibo = True
                    elif len(content_full) == 2:
                        txt_sel = content_full[0]
                        retweet_txt_sel = content_full[1]
                        is_long_weibo = True
                        is_long_retweet = True
                    elif retweet_sel[0].xpath('.//p[@node-type="feed_list_content_full"]'):
                        retweet_txt_sel = retweet_sel[0].xpath('.//p[@node-type="feed_list_content_full"]')[0]
                        is_long_retweet = True
                    else:
                        txt_sel = content_full[0]
                        is_long_weibo = True
                text = txt_sel.xpath('.//text()')
                if text is not None:
                    weibo['text'] = ' '.join(text)
                else:
                    weibo['text'] = ''
                # weibo['text'] = txt_sel.xpath('string(.)')

                weibo['article_url'] = self._get_article_url(txt_sel)
                weibo['location'] = self._get_location(txt_sel)
                if weibo['location']:
                    weibo['text'] = weibo['text'].replace(
                        '2' + weibo['location'], '')
                weibo['text'] = re.sub(r'\s+', ' ', weibo['text'][2:], flags=re.M)
                if is_long_weibo:
                    weibo['text'] = weibo['text'][:-6]
                weibo['text'] = weibo['text'].strip()
                weibo['at_users'] = self._get_at_users(txt_sel)
                weibo['topics'] = self._get_topics(txt_sel)

                # 获取转发数
                reposts_count = sel.xpath('.//a[@action-type="feed_list_forward"]/text()')
                if len(reposts_count) != 0:
                    reposts_count = reposts_count[0]
                    try:
                        reposts_count = re.findall(r'\d+.*', reposts_count)
                    except TypeError:
                        print('cookie无效或已过期，请按照'
                              'https://github.com/dataabc/weibo-search#如何获取cookie'
                              ' 获取cookie')
                        raise CookieInvalidException
                    weibo['reposts_count'] = reposts_count[0] if reposts_count else '0'
                else:
                    weibo['reposts_count'] = '0'
                # 获取评论数
                comments_count = sel.xpath('.//a[@action-type="feed_list_comment"]/text()')
                if len(comments_count) != 0:
                    comments_count = comments_count[0]
                    comments_count = re.findall(r'\d+.*', comments_count)
                    weibo['comments_count'] = comments_count[0] if comments_count else '0'
                else:
                    weibo['comments_count'] = '0'
                # 获取点赞数
                attitudes_count = sel.xpath('(.//a[@action-type="feed_list_like"])[last()]/em/text()')
                if len(attitudes_count) != 0:
                    attitudes_count = attitudes_count[0]
                    weibo['attitudes_count'] = attitudes_count if attitudes_count else '0'
                else:
                    weibo['attitudes_count'] = '0'

                created_at = sel.xpath(
                    '(.//p[@class="from"])[last()]/a[1]/text()')[0].replace(' ', '').replace('\n', '').split('前')[0]
                weibo['created_at'] = utils.standardize_date(created_at)
                try:
                    source = sel.xpath('(.//p[@class="from"])[last()]/a[2]/text()')[0]
                except IndexError:
                    source = None
                weibo['source'] = source if source else ''
                pics = ''
                is_exist_pic = sel.xpath('.//div[@class="media media-piclist"]')
                if is_exist_pic:
                    pics = is_exist_pic[0].xpath('ul[1]/li/img/@src')
                    pics = [pic[2:] for pic in pics]
                    pics = [re.sub(r'/.*?/', '/large/', pic, 1) for pic in pics]
                    pics = ['http://' + pic for pic in pics]
                video_url = ''
                is_exist_video = sel.xpath('.//div[@class="thumbnail"]/a/@action-data')
                if is_exist_video:
                    video_url = is_exist_video[0]
                    video_url = unquote(
                        str(video_url)).split('video_src=//')[-1]
                    video_url = 'http://' + video_url
                if not retweet_sel:
                    weibo['pics'] = pics
                    weibo['video_url'] = video_url
                else:
                    weibo['pics'] = ''
                    weibo['video_url'] = ''
                weibo['retweet_id'] = ''
                if retweet_sel and retweet_sel[0].xpath(
                        './/div[@node-type="feed_list_forwardContent"]/a[1]'):
                    retweet = dict()
                    retweet['retweet_id'] = retweet_sel[0].xpath(
                        './/a[@action-type="feed_list_like"]/@action-data'
                    )[0][4:]
                    retweet['weibo_id'] = retweet_sel[0].xpath(
                        './/p[@class="from"]/a/@href')[0].split(
                        '/')[-1].split('?')[0]
                    info = retweet_sel[0].xpath(
                        './/div[@node-type="feed_list_forwardContent"]/a[1]'
                    )[0]
                    retweet['user_id'] = info.xpath('@href')[0].split('/')[-1]
                    retweet['screen_name'] = info.xpath('@nick-name')[0]
                    retweet['text'] = ' '.join(retweet_txt_sel.xpath('.//text()')).replace('\u200b', '').replace('\ue627', '')
                    retweet['article_url'] = self._get_article_url(retweet_txt_sel)
                    retweet['location'] = self._get_location(retweet_txt_sel)
                    if retweet['location']:
                        retweet['text'] = retweet['text'].replace('2' + retweet['location'], '')
                    retweet['text'] = re.sub(r'\s+', ' ', retweet['text'][2:], flags=re.M).strip()
                    if is_long_retweet:
                        retweet['text'] = retweet['text'][:-6]
                    retweet['text'] = retweet['text'].strip()
                    retweet['at_users'] = self._get_at_users(retweet_txt_sel)
                    retweet['topics'] = self._get_topics(retweet_txt_sel)

                    # 获取转发数
                    reposts_count = retweet_sel[0].xpath('.//ul[@class="act s-fr"]/li/a[1]/text()')
                    if len(reposts_count) != 0:
                        reposts_count = reposts_count[0]
                        reposts_count = re.findall(r'\d+.*', reposts_count)
                        retweet['reposts_count'] = reposts_count[0] if reposts_count else '0'
                    else:
                        retweet['reposts_count'] = '0'
                    # 获取评论数
                    comments_count = retweet_sel[0].xpath('.//ul[@class="act s-fr"]/li[2]/a[1]/text()')
                    if len(comments_count) != 0:
                        comments_count = comments_count[0]
                        comments_count = re.findall(r'\d+.*', comments_count)
                        retweet['comments_count'] = comments_count[0] if comments_count else '0'
                    else:
                        retweet['comments_count'] = '0'
                    # 获取点赞数
                    attitudes_count = retweet_sel[0].xpath('.//a[@action-type="feed_list_like"]/em/text()')
                    if len(attitudes_count) != 0:
                        attitudes_count = attitudes_count[0]
                        retweet['attitudes_count'] = attitudes_count if attitudes_count else '0'
                    else:
                        retweet['attitudes_count'] = '0'

                    created_at = retweet_sel[0].xpath(
                        './/p[@class="from"]/a[1]/text()')[0].replace(' ', '').replace('\n', '').split('前')[0]
                    retweet['created_at'] = utils.standardize_date(created_at)
                    source = retweet_sel[0].xpath(
                        './/p[@class="from"]/a[2]/text()')
                    retweet['source'] = source[0] if source else ''
                    retweet['pics'] = pics
                    retweet['video_url'] = video_url
                    weibo['retweet_id'] = retweet['retweet_id']
                    weibo['retweet'] = retweet
                # print(weibo)
                yield weibo

    @staticmethod
    def _get_article_url(selector):
        """获取微博头条文章url"""
        article_url = ''
        text = selector.xpath('string(.)')[0].replace(
            '\u200b', '').replace('\ue627', '').replace('\n',
                                                        '').replace(' ', '')
        if text.startswith('发布了头条文章'):
            urls = selector.xpath('.//a')
            for url in urls:
                if url.xpath(
                        'i[@class="wbicon"]/text()')[0] == 'O':
                    if url.xpath('@href')[0] and url.xpath(
                            '@href')[0].startswith('http://t.cn'):
                        article_url = url.xpath('@href')[0]
                    break
        return article_url

    @staticmethod
    def _get_location(selector):
        """获取微博发布位置"""
        a_list = selector.xpath('.//a')
        location = ''
        for a in a_list:
            if a.xpath('./i[@class="wbicon"]') and a.xpath(
                    './i[@class="wbicon"]/text()')[0] == '2':
                location = a.xpath('string(.)')[1:]
                break
        return location

    @staticmethod
    def _get_at_users(selector):
        """获取微博中@的用户昵称"""
        a_list = selector.xpath('.//a')
        at_list = []
        for a in a_list:
            if len(unquote(a.xpath('@href')[0])) > 14 and len(
                    a.xpath('string(.)')) > 1:
                if unquote(a.xpath('@href')[0])[14:] == a.xpath(
                        'string(.)')[1:]:
                    at_user = a.xpath('string(.)')[1:]
                    if at_user not in at_list:
                        at_list.append(at_user)
        return at_list

    @staticmethod
    def _get_topics(selector):
        """获取参与的微博话题"""
        a_list = selector.xpath('.//a')
        topics = ''
        topic_list = []
        for a in a_list:
            text = a.xpath('string(.)')
            if len(text) > 2 and text[0] == '#' and text[-1] == '#':
                if text[1:-1] not in topic_list:
                    topic_list.append(text[1:-1])
        if topic_list:
            topics = ','.join(topic_list)
        return topics
