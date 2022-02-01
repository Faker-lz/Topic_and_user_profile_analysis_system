import json

import pymongo
import requests
from bson import ObjectId
from celery_task import celeryapp
from celery_task.utils import mongo_client
from celery_task.config import mongo_conf

MONGO_DB = "test"

# myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
# mydb = myclient[MONGO_DB]
# col_repost = mydb[mongo_conf.COMMENT_REPOSTS]
# col_tree = mydb[mongo_conf.COMMENT_TREE]
col_repost = mongo_client.db[mongo_conf.COMMENT_REPOSTS]
col_tree = mongo_client.db[mongo_conf.COMMENT_TREE]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
    'Accept': "*/*",
    "Accept-Encoding": "gzip, deflate, br"
}


class MyTree:
    def __init__(self, root_node):
        """
        :param root_node: 传播树根节点
        {"user_id": 0,
         "user_name": "程逸风",
         "content": "",
         "children": {}}
        """
        self.tree = root_node

    def append_point_to_tree(self, path, end_node):
        """
        将一条路径组织为树，路径为节点的列表
        :param path: 路径
        :param end_node: 末端节点
        :return:
        """
        now_position = self.tree
        index = 0
        while index < len(path):
            if now_position["children"].__contains__(path[index]["user_name"].strip()):
                now_position = now_position["children"][path[index]["user_name"].strip()]
                index += 1

            else:
                # 创建新节点
                now_position["children"][path[index]["user_name"].strip()] = {"user_id": 0,
                                                                              "user_name": path[index][
                                                                                  "user_name"].strip(),
                                                                              "content": path[index]["content"],
                                                                              "children": {}}

        # 添加end节点信息
        if now_position["children"].__contains__(end_node["user_name"].strip()):
            now_position["children"][end_node["user_name"].strip()]["user_id"] = end_node["user_id"]
            index += 1

        else:
            # 创建新节点
            now_position["children"][end_node["user_name"].strip()] = {"user_id": end_node["user_id"],
                                                                       "user_name": end_node["user_name"].strip(),
                                                                       "content": end_node["content"],
                                                                       "children": {}}
        return self.tree

    # 多条路径一次性插入到树中
    def insert_list_to_tree(self, paths):
        for path in paths:
            path["repost"].reverse()
            print(path)
            print(path["repost"])
            end_node = {"user_id": path["user_id"],
                        "user_name": path["user_name"].strip(),
                        "content": path["content"],
                        "children": {}}
            self.append_point_to_tree(path["repost"], end_node)

    def get_tree(self):
        return self.tree


def get_root_node(tag_comment_task_id="1629963031KukLkmL4i"):
    weibo_dict = mongo_client.db[mongo_conf.COMMENT_TASK].find_one({
        'tag_comment_task_id': tag_comment_task_id, 'weibo_id': tag_comment_task_id[10:]
    })
    print('get_root_node', weibo_dict)
    if weibo_dict.get('detail'):
        return {
            "user_id": weibo_dict['detail']["user_id"],
            "user_name": weibo_dict['detail']["user_name"].strip(),
            "content": weibo_dict['detail']["weibo_content"],
            "children": {}
        }
    else:
        return {
            'user_id': '',
            'user_name': '',
            'content': '',
            'children': {}
        }


def init_tree_doc(task_id):
    return col_tree.insert({"tag_comment_task_id": task_id, "data": {}})


@celeryapp.task(bind=True)
def get_path_tree(self, task_id, doc_id):
    my_tree = MyTree(get_root_node(task_id))
    myquery = {"task_id": task_id}
    mydoc = col_repost.find(myquery)
    for index, path in enumerate(mydoc):
        path["repost"].reverse()
        end_node = {"user_id": path["user_id"],
                    "user_name": path["user_name"].strip(),
                    "content": path["content"],
                    "children": {}}
        my_tree.append_point_to_tree(path["repost"], end_node)
        self.update_state(state='PROGRESS',
                          meta={'current': index + 1, 'total': mydoc.count(), 'task_id': task_id})
        if (index + 1) % 500 == 0:
            col_tree.update_one({"_id": ObjectId(doc_id)}, {"$set": {"data": my_tree.get_tree()}})
    col_tree.update_one({"_id": ObjectId(doc_id)}, {"$set": {"data": my_tree.get_tree()}})
    # with open("./data1.json", "w", encoding="utf-8") as f:
    #     json.dump(my_tree.get_tree(), f, ensure_ascii=False)


def get_path_tree_part(tag_comment_task_id, doc_id):
    my_tree = MyTree(get_root_node(tag_comment_task_id))
    myquery = {"tag_comment_task_id": tag_comment_task_id}
    mydoc = col_repost.find(myquery)
    for index, path in enumerate(mydoc):
        path["repost"].reverse()
        end_node = {"user_id": path.get("user_id"),
                    "user_name": path.get("user_name".strip()),
                    "content": path.get("content"),
                    "children": {}}
        my_tree.append_point_to_tree(path["repost"], end_node)
        if (index + 1) % 500 == 0:
            col_tree.update_one({"_id": ObjectId(doc_id)}, {"$set": {"data": my_tree.get_tree()}})
    col_tree.update_one({"_id": ObjectId(doc_id)}, {"$set": {"data": my_tree.get_tree()}})


# 转换tree数据结构
def editJson(item):
    children_list = [i for i in item["children"].values()]
    item["children"] = children_list
    item["name"] = item.pop("user_name")
    item["value"] = item.pop("content")
    item.pop("user_id")
    for i in item["children"]:
        editJson(i)


def get_tree_data(task_id):
    try:
        data = col_tree.find_one({'tag_comment_task_id': task_id})
        if data:
            editJson(data['data'])
            return {'tag_comment_task_id': data['tag_comment_task_id'], 'data': data['data']}
    except Exception as e:
        return {"error": str(e)}


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


def node(task_id):
    try:
        nodes = set()
        edges = {}
        data = col_tree.find_one({'tag_comment_task_id': task_id})
        if data:
            editJson4Graph(data['data'], nodes, edges)
            # return {'task_id': data['task_id'], 'data': data['data']}
    except Exception as e:
        return {"error": str(e)}



if __name__ == '__main__':
    """
    未解决问题：1 根节点信息获取 √ 4/2
              2 末尾节点信息添加 √ 4/2
              3 末尾节点修改树信息 √ 4/2
              
    参数：任务id(时间戳+微博id)
    """
    # my_tree = MyTree(get_root_node("K7okwxcKa"))
    # myquery = {"task_id": 1617330888}
    # mydoc = col_repost.find(myquery)
    # my_tree.insert_list_to_tree(mydoc)
    #
    # with open("../data1.json", "w", encoding="utf-8") as f:
    #     json.dump(my_tree.get_tree(), f)
    test = get_root_node()
    node("1622465660KhQes4VMs")
