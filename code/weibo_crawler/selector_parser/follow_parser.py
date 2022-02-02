import utils
from .base_parser import BaseParser

class FollowParser(BaseParser):
    """
    解析关注列表页
    """
    def __init__(self, response):
        super().__init__(response)


    def get_follows(self):
        """获取本页全部follow的信息"""
        follow_list = list()
        follow_nodes = self.selector.xpath(r'/html/body/table')
        for node in follow_nodes:
            a_follow = self.get_one_follow(node)
            if a_follow is not None:
                follow_list.append(a_follow)
        return follow_list


    def get_one_follow(self, follow_node):
        return utils.extract_from_one_table_node(follow_node)


    def get_max_page_num(self):
        """
        获取总页数
        """
        total_page_num = ''.join(self.selector.xpath(r'//div[@id="pagelist"]/form/div/text()'))
        total_page_num = total_page_num[total_page_num.rfind(r'/') + 1: total_page_num.rfind('页')]
        return int(total_page_num)
