"""
:配置类
@author: lingzhi
* @date 2021/8/12 20:29
"""
from pydantic import BaseSettings


class CeleryConfig(BaseSettings):
    """
    celery 启动的相关配置
    """
    BROKER = 'redis://localhost:6379/0'
    BACKEND = 'redis://localhost:6379/1'


class MongoConfig(BaseSettings):
    """
    Mongo的相关配置
    """
    HOST: str = '127.0.0.1'
    PORT: int = 27017
    DB_NAME: str = 'test'

    # 话题任务数据库名称
    TASK: str = 'tag_task'
    BLOG: str = 'blog'
    CHARACTER: str = 'character_category'
    EVOLVE: str = 'tag_evolve'
    HOT: str = 'tag_hot'
    INTRODUCE: str = 'tag_introduce'
    RELATION: str = 'tag_relation_graph'
    RETWEET: str = 'tag_weibo_task'
    CLOUD: str = 'tag_word_cloud'
    USER: str = 'tag_user'

    # 评论任务数据库名称
    COMMENT_TASK = 'comment_task'
    COMMENT_REPOSTS = 'comment_reposts'
    COMMENT_CLOUD = 'comment_cloud'
    COMMENT_CLUSTER = 'comment_cluster'
    COMMENT_NODE = 'comment_node'
    COMMENT_TENDENCY = 'comment_tendency'
    COMMENT_TOPIC = 'comment_topic'
    COMMENT_TREE = 'comment_tree'


class ElasticSearchConfig(BaseSettings):
    """
    ES配置
    """
    ES_HOST = '127.0.0.1:9200'
    ES_SEARCH_INDEX = 'weibo'
    ES_TIMEOUT = 60
    LANG_TYPE = ['zh', 'en']
