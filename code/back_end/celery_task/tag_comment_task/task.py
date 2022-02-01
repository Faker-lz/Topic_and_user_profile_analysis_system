"""
task，将模型与数据处理部分分离
计划仅由本文件提供task任务
"""
import time
import json
import pymongo
import requests
from bson import ObjectId

from celery_task.config import mongo_conf
from celery_task.utils import mongo_client

from celery_task import celeryapp
from celery_task.tag_comment_task.process import get_path_tree_part
from celery_task.utils.gsdmmCluster.cluster_extract import cluster_extract
from celery_task.tag_comment_task.my_cloud import preContent
from celery_task.tag_comment_task.myRank import startRank
from celery_task.tag_comment_task.repost_spider import  spider_list
from celery_task.utils.my_db import Mongo


def init_task(tag_comment_task_dict):
    """
    # 微博评论任务id的储存
    :param tag_comment_task_dict:
    :return:
    """
    tree_id = mongo_client.db[mongo_conf.COMMENT_TREE].insert_one(
        {"tag_comment_task_id": tag_comment_task_dict["tag_comment_task_id"]})
    cluster_id = mongo_client.db[mongo_conf.COMMENT_CLUSTER].insert_one(
        {"tag_comment_task_id": tag_comment_task_dict["tag_comment_task_id"]})
    cloud_id = mongo_client.db[mongo_conf.COMMENT_CLOUD].insert_one(
        {"tag_comment_task_id": tag_comment_task_dict["tag_comment_task_id"]})
    tendency_id = mongo_client.db[mongo_conf.COMMENT_TENDENCY].insert_one(
        {"tag_comment_task_id": tag_comment_task_dict["tag_comment_task_id"]})
    key_node_id = mongo_client.db[mongo_conf.COMMENT_NODE].insert_one(
        {"tag_comment_task_id": tag_comment_task_dict["tag_comment_task_id"]})

    tag_comment_task_dict["tree_id"] = str(tree_id.inserted_id)
    tag_comment_task_dict["cluster_id"] = str(cluster_id.inserted_id)
    tag_comment_task_dict["cloud_id"] = str(cloud_id.inserted_id)
    tag_comment_task_dict["tendency_id"] = str(tendency_id.inserted_id)
    tag_comment_task_dict["key_node_id"] = str(key_node_id.inserted_id)

    return tag_comment_task_dict


# 获取微博详细信息
def get_post_detail(weibo_id: str, tag_comment_task_id: str):
    response = requests.get("http://127.0.0.1:8000/weibo_curl/api/statuses_show?weibo_id={weibo_id}".
                            format(weibo_id=weibo_id))
    weibo_dict = json.loads(response.text)
    mongo_client.db[mongo_conf.COMMENT_TASK].update_one({'tag_comment_task_id': tag_comment_task_id},
                            {"$set": {'detail': weibo_dict["data"]["result"]}})



# 聚类任务
def run_by_task_id_part(tag_comment_task_id, doc_id):
    post_list = []
    for post in mongo_client.db[mongo_conf.COMMENT_REPOSTS].find({'tag_comment_task_id': tag_comment_task_id}):
        if post['content'].strip() == "" or post['content'].strip() == "转发微博":
            continue
        post_list.append({'_id': post['_id'], 'fulltext': post['content']})
    result = cluster_extract(post_list)
    mydict = result.to_dict(orient='index')
    key_list = list(mydict.keys())
    for key in key_list:
        mydict[str(key)] = mydict.pop(key)
        while '' in mydict[str(key)]["content"]:
            mydict[str(key)]["content"].remove('')
    mongo_client.db[mongo_conf.COMMENT_CLUSTER].update_one({"_id": ObjectId(doc_id)}, {"$set": {"data": mydict}})


# 调度任务
@celeryapp.task(bind=True)
def comment_task_schedule(self, tag_comment_task_dict):
    print(tag_comment_task_dict)
    # 爬虫任务
    print('开始爬虫任务')
    self.update_state(state='PROGRESS',
                      meta={'current': "爬虫任务", 'weibo_id': tag_comment_task_dict['weibo_id'],
                            'task_id': tag_comment_task_dict['tag_comment_task_id']})
    get_post_detail(weibo_id=tag_comment_task_dict['weibo_id'], tag_comment_task_id=tag_comment_task_dict['tag_comment_task_id'])
    spider_list(tag_task_id=tag_comment_task_dict['tag_task_id'], weibo_id=tag_comment_task_dict['weibo_id'],
                     tag_comment_task_id=tag_comment_task_dict['tag_comment_task_id'])
    print('爬虫任务结束')
    print('开始传播树构建任务')
    self.update_state(state='PROGRESS',
                      meta={'current': "传播树构建任务", 'weibo_id': tag_comment_task_dict['weibo_id'],
                            'task_id': tag_comment_task_dict['tag_comment_task_id']})
    get_path_tree_part(tag_comment_task_id=tag_comment_task_dict['tag_comment_task_id'],
                       doc_id=tag_comment_task_dict['tree_id'])
    print('传播树构建任务结束')
    print('开始主题挖掘任务')
    self.update_state(state='PROGRESS',
                      meta={'current': "传播分析-主题挖掘", 'weibo_id': tag_comment_task_dict['weibo_id'],
                            'task_id': tag_comment_task_dict['tag_comment_task_id']})
    run_by_task_id_part(tag_comment_task_id=tag_comment_task_dict['tag_comment_task_id'],
                        doc_id=tag_comment_task_dict['cluster_id'])
    print('主题挖掘任务结束')
    print('开始传播分析-词云任务')
    self.update_state(state='PROGRESS',
                      meta={'current': "传播分析-词云", 'weibo_id': tag_comment_task_dict['weibo_id'],
                            'task_id': tag_comment_task_dict['tag_comment_task_id']})
    preContent(tag_comment_task_id=tag_comment_task_dict['tag_comment_task_id'], doc_id=tag_comment_task_dict['cloud_id'])
    print('传播分析-词云任务结束')
    print('开始传播分析-趋势任务')
    self.update_state(state='PROGRESS',
                      meta={'current': "传播分析-趋势", 'weibo_id': tag_comment_task_dict['weibo_id'],
                            'task_id': tag_comment_task_dict['tag_comment_task_id']})
    spreadTendency(tag_comment_task_id=tag_comment_task_dict['tag_comment_task_id'],
                   doc_id=tag_comment_task_dict['tendency_id'])
    print('传播分析-趋势任务结束')
    print('开始传播分析-关键节点任务')
    self.update_state(state='PROGRESS',
                      meta={'current': "传播分析-关键节点", 'weibo_id': tag_comment_task_dict['weibo_id'],
                            'task_id': tag_comment_task_dict['tag_comment_task_id']})
    node(tag_comment_task_id=tag_comment_task_dict['tag_comment_task_id'])


# 初始化任务
def start_task(tag_task_id: str, weibo_post=None):
    # todo 错误处理
    # 时间戳->字符串
    time_int = int(time.time())
    time_array = time.localtime(time_int)
    time_style_str = time.strftime("%Y-%m-%d %H:%M:%S", time_array)

    tag_comment_task_id = str(time_int) + weibo_post['weibo_id']
    task_dict = {"tag_task_id": tag_task_id, "weibo_id": weibo_post['weibo_id'],
                 "tag_comment_task_id": tag_comment_task_id,
                 'created_time': time_style_str}

    task_dict = init_task(task_dict)

    task = comment_task_schedule.delay(tag_comment_task_dict=task_dict)
    task_dict['celery_id'] = task.id
    # weibo_detail = get_post_detail(weibo_id=weibo_id)
    task_dict["detail"] = weibo_post
    task_dict["analysis_status"] = "PENDING"
    mongo_client.db[mongo_conf.COMMENT_TASK].insert_one(task_dict)
    task_dict.pop("_id")
    print(task_dict)
    return task_dict


# 刷新任务
def refresh_task():
    mydb = mongo_client.db[mongo_conf.COMMENT_TASK]
    for item in mydb.find():
        try:
            if item['analysis_status'] != "SUCCESS":
                task = celeryapp.AsyncResult(item['celery_id'])
                if task.state == "PROGRESS":
                    mydb.update_one({"_id": item['_id']},
                                            {"$set": {"analysis_status": task.info.get('current', 0)}})
                else:
                    mydb.update_one({"_id": item['_id']}, {"$set": {"analysis_status": task.state}})
        except Exception:
            print(item['tag_comment_task_id'], '刷新任务失败')
            print(item)


# 获取任务队列
def getTaskList():
    result = {"error_code": 0, "error_msg": "", "data": []}
    # 获取task库,更新task状态
    mydb = mongo_client.db[mongo_conf.COMMENT_TASK]
    for item in mydb.find():
        try:
            if item['analysis_status'] != "SUCCESS":
                task = celeryapp.AsyncResult(item['celery_id'])
                if task.state == "PROGRESS":
                    item['analysis_status'] = task.info.get('current', 0)
                    mydb.update_one({"_id": item['_id']},
                                            {"$set": {"analysis_status": task.info.get('current', 0)}})
                else:
                    item['analysis_status'] = task.state
                    mydb.update_one({"_id": item['_id']}, {"$set": {"analysis_status": task.state}})
            item.pop("_id")
            result["data"].append(item)
        except Exception as e:
            print(e)
            print(item)
    return result


# 删除任务
def deleteTask(tag_comment_task_id):
    mydb = mongo_client.db[mongo_conf.COMMENT_TASK]
    celeryapp.control.revoke(tag_comment_task_id, terminate=True)
    myquery = {"tag_comment_task_id": tag_comment_task_id}
    mydb.delete_one(myquery)
    mongo_client.db[mongo_conf.COMMENT_TREE].delete_one(myquery)
    mongo_client.db[mongo_conf.COMMENT_CLUSTER].delete_one(myquery)


# 统计每天的转发
def spreadTendency(tag_comment_task_id=None, doc_id=None):
    # if task_id is None or task_id.__len__() == 0:
    #     return {"error_code": 1, "error_msg": "缺少task_id"}
    pipeline = [{'$project': {'day': {'$substr': ["$created_at", 0, 10]}, 'tag_comment_task_id': '$tag_comment_task_id'}},
                {'$group': {'_id': {'data': '$day', 'tag_comment_task_id': '$tag_comment_task_id'}, 'count': {'$sum': 1}}},
                {'$sort': {"_id.data": 1}},
                {'$match': {'_id.tag_comment_task_id': tag_comment_task_id}}
                ]
    result = []
    mydb = mongo_client.db[mongo_conf.COMMENT_REPOSTS]
    for i in mydb.aggregate(pipeline):
        print('reports:', i)
        result.append({"key": i['_id']["data"], "doc_count": i["count"]})
    mongo_client.db[mongo_conf.COMMENT_TENDENCY].update_one({"tag_comment_task_id": tag_comment_task_id},
                                                    {"$set": {"data": result}})


# 以task_id获取 趋势 内容
def getByTendencyId(tag_comment_task_id=None):
    item = mongo_client.db[mongo_conf.COMMENT_TENDENCY].find_one({"tag_comment_task_id": tag_comment_task_id})
    item.pop("_id")
    data_time = []
    data_count = []
    for i in item["data"]:
        data_time.append(i["key"])
        data_count.append(i["doc_count"])
    data = {"data_time": data_time, "data_count": data_count}
    item["data"] = data
    print(item)
    return item


# 以task_id获取 词云 内容
def getByCloudId(tag_comment_task_id=None):
    # item = mydb['cloud'].find_one({"_id": ObjectId(doc_id)})
    item = mongo_client.db[mongo_conf.COMMENT_CLOUD].find_one({"tag_comment_task_id": tag_comment_task_id})
    item.pop("_id")
    print(item)
    return item


# 以task_id 获取 聚类 内容
def getByClusterId(tag_comment_task_id=None):
    # item = mydb['cluster'].find_one({"tag_comment_task_id": ObjectId(doc_id)})
    item = mongo_client.db[mongo_conf.COMMENT_CLOUD].find_one({"tag_comment_task_id": tag_comment_task_id})
    item.pop("_id")
    print(item)
    return item


# 以task_id 获取 聚类 类别
def getTypeByClusterId(tag_comment_task_id=None):
    item = mongo_client.db[mongo_conf.COMMENT_CLUSTER].find_one({"tag_comment_task_id": tag_comment_task_id})
    item.pop("_id")
    result = []
    for i in item['data']:
        key_count = {'key': item['data'][i]['key'],
                     'doc_count': len(item['data'][i]['id'])}
        result.append(key_count)
    return result


# 以task_id和类别 获取 某一类聚类内容
def getContentByClusterId(tag_comment_task_id=None, content_type=None):
    item = mongo_client.db[mongo_conf.COMMENT_CLUSTER].find_one({"tag_comment_task_id": tag_comment_task_id})
    item.pop("_id")
    result = []
    for i in item['data']:
        if item['data'][i]['key'] == content_type:
            result = item['data'][i]['content']
    result_sort = []

    for content in result:
        content_sort = {"text": content, "score": len(set(content)) / 8}
        for key in content_type.split(" "):
            if key in content:
                content_sort["score"] += 1
        result_sort.append(content_sort)
    result_sort.sort(key=lambda i: i['score'], reverse=True)
    return result_sort[0:10]


# 以task_id和类别 获取 某一类聚类内容
def getPostById(tag_comment_task_id=None):
    item = mongo_client.db[mongo_conf.COMMENT_TASK].find_one({"tag_comment_task_id": tag_comment_task_id})
    result = []
    result.append(item["detail"])
    return result


# 统计关键节点
def statisticsRepost(item, total):
    children_list = [i for i in item["children"].values()]
    total[item['user_name'].strip()] = len(children_list)
    for i in children_list:
        total[item['user_name'].strip()] = total[item['user_name'].strip()] + statisticsRepost(i, total)
    return total[item['user_name'].strip()]


# 获取获取关键节点
def getKeyNode(tag_comment_task_id):
    item = mongo_client.db[mongo_conf.COMMENT_NODE].find_one({"tag_comment_task_id": tag_comment_task_id})
    return item['data']


# 转换tree数据结构-->leader rank 数据结构
def editJson4Graph(item, nodes, edges):
    nodes.add(item['user_name'].strip())
    if item['children']:
        edges[item['user_name'].strip()] = {}
        children_list = [i for i in item["children"].values()]

        for i in children_list:
            editJson4Graph(i, nodes, edges)
            i.pop("children")
            edges[item['user_name'].strip()][i["user_name"].strip()] = i


# leader rank计算
def node(tag_comment_task_id):
    try:
        nodes = set()
        edges = {}
        re_edges = {}
        data = mongo_client.db[mongo_conf.COMMENT_TREE].find_one({'tag_comment_task_id': tag_comment_task_id})
        if data:
            total = {}
            statisticsRepost(data['data'], total)

            editJson4Graph(data['data'], nodes, edges)
            # 去除G节点和根节点
            result_sorted = startRank(edges, re_edges, list(nodes))[2:]
            result_list = []
            for item in result_sorted:
                try:
                    if total[item[0]] != 0:
                        result = {"name": item[0], "count": total[item[0]], "score": item[1]}
                        result_list.append(result)
                except:
                    # todo
                    pass
            mongo_client.db[mongo_conf.COMMENT_NODE].update_one({"tag_comment_task_id": tag_comment_task_id},
                                                        {"$set": {"data": result_list}})
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # mydb['tendency'].insert_one(spreadTendency("1621162456K7okwxcKa"))
    # refresh_task()
    # print(getTaskList())
    # print(node("1622465660KhQes4VMs"))
    run_by_task_id_part('1635758101KDOBs1AO2', '617fb015de0c993aa08e78f0')