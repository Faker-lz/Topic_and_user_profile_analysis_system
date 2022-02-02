from datetime import datetime, timedelta
import sys
from settings import LOGGING
import traceback


def report_log(exception: Exception):
    """
    将错误报告给日志
    :param exception: 产生的异常
    """
    LOGGING.warning(
        '{} occur a exception {}:\n{}\n==========\n{}'
        .format(datetime.now(), exception.__class__.__name__, exception.args, traceback.format_exc())
    )


def handle_garbled(info):
    """处理乱码"""
    try:
        _info = (' '.join(info.xpath('.//text()')).replace(u'\u200b', '').encode(
            sys.stdout.encoding, 'ignore').decode(sys.stdout.encoding))
        return _info
    except Exception as e:
        LOGGING.exception(e)


def extract_from_one_table_node(table_node):
    """处理关注者或粉丝列表页中的一个table"""
    table_node = table_node.xpath('.//td')[1]
    follow_user = table_node.xpath('./a')[0]
    user_name = follow_user.text  # 关注者的昵称
    user_id = follow_user.get('href')  # 关注者的id
    if isinstance(user_id, str):
        user_id = user_id[user_id.rfind(r'/') + 1:]
    fans_num = table_node.xpath('text()')  # 关注者的粉丝数
    if len(fans_num) != 0:
        # fans_num = str(fans_num[0])
        fans_num = int(fans_num[0][2: -1])
    else:
        fans_num = None
    return dict(user_id=user_id, user_name=user_name, fans_num=fans_num)


def standardize_date(created_at):
    """标准化微博发布时间"""
    if "刚刚" in created_at:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    elif "秒" in created_at:
        second = created_at[:created_at.find(u"秒")]
        second = timedelta(seconds=int(second))
        created_at = (datetime.now() - second).strftime("%Y-%m-%d %H:%M")
    elif "分钟" in created_at:
        minute = created_at[:created_at.find(u"分钟")]
        minute = timedelta(minutes=int(minute))
        created_at = (datetime.now() - minute).strftime("%Y-%m-%d %H:%M")
    elif "小时" in created_at:
        hour = created_at[:created_at.find(u"小时")]
        hour = timedelta(hours=int(hour))
        created_at = (datetime.now() - hour).strftime("%Y-%m-%d %H:%M")
    elif "今天" in created_at:
        today = datetime.now().strftime('%Y-%m-%d')
        created_at = today + ' ' + created_at[2:]
    elif '年' not in created_at:
        year = datetime.now().strftime("%Y")
        month = created_at[:2]
        day = created_at[3:5]
        time = created_at[6:]
        created_at = year + '-' + month + '-' + day + ' ' + time
    else:
        year = created_at[:4]
        month = created_at[5:7]
        day = created_at[8:10]
        time = created_at[11:]
        created_at = year + '-' + month + '-' + day + ' ' + time
    return created_at
