"""
:处理前端tag热度请求
@author: lingzhi
* @date 2021/8/13 14:55
"""
import gopup as gp
from motor.motor_asyncio import AsyncIOMotorDatabase
from models.dto.tag_dto.tag_hot import TagHot


async def update_hot_data(tag_task_id: str, mongo_db: AsyncIOMotorDatabase) -> TagHot:
    """
    当接收到前端热度请求后，获取并更新热度信息
    :param mongo_db: 数据库参数
    :param tag_task_id: tag任务id
    :return:
    """
    # TODO 错误处理
    try:
        mongo_collection = mongo_db['tag_hot']
        hot_find = await mongo_collection.find_one({'tag_task_id': tag_task_id})
        print(tag_task_id)
        tag = hot_find['tag']

        one_day = gp.weibo_index(word=tag, time_type='1day')
        one_month = gp.weibo_index(word=tag, time_type='1month')
        three_month = gp.weibo_index(word=tag, time_type='3month')
        one_day_dict = {'data_time': list(one_day.to_dict()[tag].keys()), 'data_count': list(one_day.to_dict()[tag].values())}
        one_month_dict = {'data_time': list(one_month.to_dict()[tag].keys()), 'data_count': list(one_month.to_dict()[tag].values())}
        three_month_dict = {'data_time': list(three_month.to_dict()[tag].keys()), 'data_count': list(three_month.to_dict()[tag].values())}

        update_data = TagHot(
            tag_task_id=tag_task_id,
            tag=tag,
            one_day=one_day_dict,  # {str(time): value for time, value in one_day.to_dict()[tag].items()},
            one_month=one_month_dict,  # {str(time): value for time, value in one_month.to_dict()[tag].items()},
            three_month=three_month_dict,  # {str(time): value for time, value in three_month.to_dict()[tag].items()}
        )
        await mongo_collection.update_one({'tag_task_id': tag_task_id}, {'$set': {
            'one_day': update_data.one_day,
            'one_month': update_data.one_month,
            'three_month': update_data.three_month
        }})
        return update_data
    except AttributeError as e:
        print(e)
