"""
:话题关系网任务
@author: lingzhi
* @date 2021/7/22 16:25
"""
from functools import reduce

from celery_task.utils import mongo_client
from celery_task.config import mongo_conf


def tag_relation(weibo_data: dict, tag_task_id: str, user_mark_data: dict):
    """
    处理话题人物关系网的函数
    :param user_mark_data: 用户分类数据
    :param weibo_data:微博数据
    :param tag_task_id:话题任务
    :return:
    """
    node_list = list()
    link_list = list()
    weibo_list = reduce(lambda x, y: x if y in x else x + [y], [[], ] + weibo_data['data'])
    screen_name_set = set(i['screen_name'] for i in weibo_list)
    relation_data = list()
    for screen_name in screen_name_set:
        at_users_list = list()
        user_id = 0
        hot_count = 0
        for weibo in weibo_list:
            if weibo.get('screen_name') == screen_name:
                at_users_list.extend(weibo.get('at_users'))
                hot_count += int(weibo.get('hot_count'))
                user_id = weibo['user_id']
        relation_data.append({'screen_name': screen_name,
                             'user_id': user_id,
                             'at_users': at_users_list,
                              'hot_count': hot_count
                              }
                             )
    for data in relation_data:
        category = -1
        for user_mark in user_mark_data.get('data'):
            if user_mark.get('user_id') == data['user_id']:
                category = user_mark.get('category')
                break
        node = {'category': category, 'name': data['screen_name'], 'userId': data['user_id'], 'value': int(data['hot_count'])}
        node_list.append(node)
        for i in data['at_users']:
            link = {'source': data['screen_name'], 'target': i, 'weight': data['at_users'].count(i)}
            if link not in link_list:
                link_list.append(link)
            if i not in screen_name_set:
                node = {'category': -1, 'name': i, 'userId': None,
                        'value': int(data['hot_count'])}
                node_list.append(node)
                screen_name_set.add(i)
            else:
                for node_item in node_list:
                    if node_item['name'] == i:
                        node_item['value'] += int(data['hot_count'])
                        break
    query_by_task_id = {'tag_task_id': tag_task_id}
    update = {"$set": {'nodes_list': node_list, 'links_list': link_list, 'categories': user_mark_data.get('categories')}}
    mongo_client.db[mongo_conf.RELATION].update_one(query_by_task_id, update)
    mongo_client.db[mongo_conf.CHARACTER].update_one(query_by_task_id, {'$set': {'detail': node_list}})


if __name__ == '__main__':
    data = mongo_client.db[mongo_conf.BLOG].find_one({'tag_task_id': 'afe59eaa4a9bc41147700ae1b90e7dba'})
    tag_relation(data, 'afe59eaa4a9bc41147700ae1b90e7dba')

