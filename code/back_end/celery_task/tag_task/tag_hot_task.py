"""
:话题热度任务
@author: lingzhi
* @date 2021/7/22 16:26
"""
from celery_task.utils.gopup_utils import tendency
from celery_task.utils import mongo_client
from celery_task.config import mongo_conf
import logging


def hot_task(tag: str, tag_task_id: str):
    """
    获取话题发展趋势信息
    :param tag:
    :param tag_task_id:
    :return:
    """
    try:
        hot_one_day = tendency(tag, '1day')
        dict_one_day = hot_one_day.to_dict()
        hot_one_month = tendency(tag, '1month')
        dict_one_month = hot_one_month.to_dict()
        hot_three_month = tendency(tag, '3month')
        dict_three_month = hot_three_month.to_dict()
        final_dict = {'tag': tag, 'one_day': {str(time): value for time, value in dict_one_day[tag].items()},
                      'one_month': {str(time): value for time, value in dict_one_month[tag].items()},
                      'three_month': {str(time): value for time, value in dict_three_month[tag].items()}}
        query_by_id = {'tag_task_id': tag_task_id}
        update_data = {"$set": final_dict}
        mongo_client.db[mongo_conf.HOT].update_one(query_by_id, update_data)
    except AttributeError as exc:
        query_by_id = {'tag_task_id': tag_task_id}
        mongo_client.db[mongo_conf.HOT].update_one(query_by_id, {"$set": {"tag": tag}})
        # TODO log
        print(exc)
        # logging.log(exc)



if __name__ == '__main__':
    hot_task('吴亦凡', '111')
