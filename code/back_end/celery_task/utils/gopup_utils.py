"""
:通过gupop库获取数据的工具包
@author: lingzhi
* @date 2021/8/12 17:15
"""
import gopup as gp
from pandas import DataFrame


def tendency(tag: str, time_type: str) -> DataFrame:
    """
    获取话题发展趋势的函数
    :param tag:
    :param time_type:
    :return:
    """
    return gp.weibo_index(word=tag, time_type=time_type)


def user(user_id: str) -> dict:
    """
    通过user_id获取该用户的详细信息
    :param user_id:
    :return:
    """
    user_data = gp.weibo_user(user_id=user_id)
    user_data_dict = user_data.to_dict()
    user_dict = {
        'user_id': user_id,
        'nickname': user_data_dict.get('用户昵称').get(1),
        'gender': user_data_dict.get('性别').get(1),
        'location': user_data_dict.get('所在地').get(1),
        'birthday': user_data_dict.get('生日').get(1),
        'description': user_data_dict.get('描述').get(1),
        'verified_reason': user_data_dict.get('微博认证').get(1),
        'education': user_data_dict.get('大学').get(1),
        'work': user_data_dict.get('公司').get(1),
        'weibo_num': user_data_dict.get('微博数').get(1),
        'followers': user_data_dict.get('粉丝数').get(1),
        'following': user_data_dict.get('关注数').get(1)

    }
    return user_dict


if __name__ == '__main__':
    print(user('2656274875'))
