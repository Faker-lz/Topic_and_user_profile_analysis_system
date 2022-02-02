from lxml import etree


class BaseParser:
    def __init__(self, response=None):
        """保存response于属性中，同时将response转化成selector"""
        self.response = response
        if response is not None:
            self.selector = etree.HTML(self.response.body)
        else:
            self.selector = None
