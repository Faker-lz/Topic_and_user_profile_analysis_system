"""
:mongo_db 的连接接口
@author: lingzhi
* @date 2021/8/8 20:03
"""
import pymongo
import motor.motor_asyncio
from elasticsearch import AsyncElasticsearch
from celery_task.config import es_conf, mongo_conf


class Mongo(object):
    """
    pymongo 统一申请类
    """

    def __init__(self, db_name=mongo_conf.DB_NAME):
        self.db_name = db_name
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.db = self.client[self.db_name]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('关闭mongo连接')
        self.client.close()


class MotorMongo(object):
    """
    异步mongodb 统一申请类
    """

    def __init__(self, collect_name, db_name=mongo_conf.DB_NAME):
        self.db_name = db_name
        self.client = motor.motor_asyncio.AsyncIOMotorClient(host='127.0.0.1', port=27017)
        print('数据库已连接')
        self.db = self.client[self.db_name]
        self.collect = self.db[collect_name]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        print('数据库关闭')


class ElasticSearchClient(object):
    """
    请求es客户端接口
    """

    def __init__(self):
        self.es_client = AsyncElasticsearch(hosts=es_conf.ES_HOST, sniff_on_start=True,
                                            sniff_on_connection_fail=True, sniffer_timeout=es_conf.ES_TIMEOUT,
                                            verify_certs=False,
                                            ssl_show_warn=False)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.es_client.close()


mongo_client = Mongo(mongo_conf.DB_NAME)
