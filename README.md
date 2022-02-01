# Topic and user profile analysis system

## 介绍

微博的**话题**、**博文**及**用户画像**分析系统。

功能:

- 微博话题博文搜索：根据用户输入关键字搜索出热度最高的50页近1000条博文

- 微博话题分析：用户可以将相关话题加入分析任务队列中，后端会异步执行分析任务(基于celery)
  
  - 话题任务列表：当前系统中的所有任务，包括分析中、完成和异常的任务。
  
  - 话题最热博文：展示出该话题下热度最高的十条博文。
  
  - 话题热度：展示该话题近一天、一个月、三个月的关注热度。
  
  - 话题词云：根据话题中爬取到的所有博文内容分析出话题关联的词语。
  
  - 话题简略传播关系图：用有向图展示出该话题的传播关系。
  
  ![avatar](https://github.com/Faker-lz/Topic_and_user_profile_analysis_system/blob/master/doc/illustration/%E8%AF%9D%E9%A2%98%E4%BB%BB%E5%8A%A1%E5%88%97%E8%A1%A8.png)

- 博文分析：对话题中热度前十的博文进行详细分析。
  
  - 博文详情：展示博文的文本内容和发博用户的粗略信息。
  
  - 
  
  - 博文关键转发节点：列出在博文传播过程中起重要扩散作用的转发节点，通常是转发后产生相对大量关注的节点。
  
  - 博文传播树：博文的转发传播树。
  
  - 博文评论词云：博文评论下关联的词语。
  
  - 博文主题分析：博文下**评论**主题及其占比。
  
  - 博文热点转发：显示关注较高的热点转发内容。
  
  ![avatar](https://github.com/Faker-lz/Topic_and_user_profile_analysis_system/blob/master/doc/illustration/%E5%8D%9A%E6%96%87%E8%AF%A6%E6%83%85.png)

- 用户画像：根据用户在**不同话题**下微博文本的聚类主题为用户打标签，逐步完善用户画像。
  
  ![artvar](https://github.com/Faker-lz/Topic_and_user_profile_analysis_system/blob/master/doc/illustration/%E8%AF%9D%E9%A2%98%E5%86%85%E7%94%A8%E6%88%B7%E6%A0%87%E7%AD%BE%E5%8F%8A%E5%85%B7%E4%BD%93%E4%BC%A0%E6%92%AD%E5%85%B3%E7%B3%BB.png)

## 设计

* 概要设计：[前端页面低保真原型设计]([墨刀](https://modao.cc/app/096f66e13ccb38c83e73e67f3fbdb091526d900b?simulator_type=outside_artboard))

* 详细设计：
  
  * 架构设计：项目整体采用BS架构实现前后端分离。前端具体使用vue框架，参照[[前端页面低保真原型设计](%5B%E5%A2%A8%E5%88%80%5D(https://modao.cc/app/096f66e13ccb38c83e73e67f3fbdb091526d900b?simulator_type=outside_artboard))来实现，后端使用python的[fastapi]([FastAPI (tiangolo.com)](https://fastapi.tiangolo.com/zh/))框架搭建，结合分布式异步任务处理框架[celery]([使用Redis - Celery 中文手册 (celerycn.io)](https://www.celerycn.io/ru-men/zhong-jian-ren-brokers/shi-yong-redis))实现任务发布和任务执行的解耦，使得异步、快速处理话题分析任务成为了可能。
  
  * 涉及算法：
    
    * 基于MGP的博文短文本聚类分析算法gsdmmCluster,用于对某一博文的**评论**进行聚类分析。
    
    * LDA，用于对话题内**舆论场**进行聚类分析。
    
    * Single_Pass，用于对话题**舆论场**进行聚类分析。
  
  * 路由、数据库设计文档：在`\doc\desgin`文件中

## 配置

* 后端配置：
  
  * 在文件`\code\back_end\config\config_class`中修改如下配置：
    
    ```
    class AppConfig(BaseSettings):
        """
        fastapi_app启动的相关配置
        """
        HOST: str = '127.0.0.1'
        PORT: int = 81
    
    
    class WeiBoConfig(BaseSettings):
    """weibo 爬虫api的相关配置"""
        BASEPATH: str = 'http://127.0.0.1:8000'
    ```
  
  * 在`\code\back_end\celery_task\config\task_config_class.py`文件中修改`celery`相关配置：
    
    ```
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
    
    ```
  
  

    

* 微博爬虫微服务配置:
  
  请参照`\code\weibo_crawler\README.md`文件进行配置

## 启动

* 后端
  
  * 安装Redis数据库
  
  * 依据项目中`requestments.txt`文件，安装好后端需要的所有依赖库
    
    > 强烈建议参照`doc\话题分析系统后端部署.docx`文件构建虚拟运行环境。
  
  * 运行`\code\back_end\main.py`启动fastapi的app
  
  * 启动Redis数据库
  
  * 进入`\code\back_end`文件夹，运行`celery -A celery_task.celeryapp  worker --loglevel=info  -P threads`命令启动`celery`

* 前端
  
  * 进入`\code\back_end`文件夹，按照`README.md`文件安装依赖。
  
  * 执行`npm install`命令安装vue项目。
  
  * 执行`npm run server`运行前端。

* 微博爬虫
  
  进入`\code\weibo_crawler`文件夹，配置好后，运行`weibo_curl_api.py`文件
