"""
:不存在异常
@author: lingzhi
* @date 2021/10/6 11:23
"""
from .base_exc import CustomBaseException


class NotExistException(CustomBaseException):
    def __init__(self, msg: str = ''):
        super().__init__('ERROR: '+msg+' NOT EXISTED!')
