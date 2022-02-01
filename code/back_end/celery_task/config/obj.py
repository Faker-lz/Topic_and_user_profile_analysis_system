"""
:配置实体
@author: lingzhi
* @date 2021/8/12 20:32
"""
from .task_config_class import (
    MongoConfig,
    CeleryConfig,
    ElasticSearchConfig
)

mongo_conf = MongoConfig()
celery_conf = CeleryConfig()
es_conf = ElasticSearchConfig()
