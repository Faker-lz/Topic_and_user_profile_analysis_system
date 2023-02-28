# weibo_curl 文档说明

## 介绍

由tornado框架以协程运行方式完成的通过**爬取新浪微博**信息来提供获取各种类型数据的web服务

## 配置方式：

1. 在`settings.py`中更改`PORT_NUM`可以指定程序运行的端口号
2. 在`settings.py`中更改`LOGGING`可以更改日志的记录位置
3. 在`account/account.json`中的`cookies`字段中填写由多个有效cookie组成的列表（Cookie获取见文档末尾），在`proxies`字段中填写由多个代理组成的列表，每个代理的格式为`[proxy_host, proxy_port]`
4. 以上配置完成后运行`weibo_curl_api.py`即可。

## 返回结果格式：

```
{
    'error_code':0,
    'data':{
        'result': {} or [],
        'cursor': str
    },
    'error_msg':''
}
```

## API

### 1. 推文搜索接口

+ 根据关键字搜索推文
+ 路由：`/weibo_curl/api/search_tweets`

#### 请求参数

URL参数：

| key     | description        | 是否必选               | example |
| ------- | ------------------ | ------------------ | ------- |
| keyword | 搜索关键字              | 是                  | '新冠肺炎'  |
| cursor  | 搜索第几页              | 否，默认第一页            | 2       |
| is_hot  | 是否搜索热门微博，1表示是，0表示否 | 否，默认为False，即搜索普通微博 | 1       |

#### 返回格式

成功时返回json的 `result` 字段为一个l由多个dict组成的list，每个dict代表一条微博，每个元素(dict)的格式如下：(每个字段默认值均为空字符串)

| key             | description     | value type      | example                                                                                                                                 |
| --------------- | --------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| head            | 该条微博的用户的头像url   | str             | "https://tvax1.sinaimg.cn/crop.0.0.700.700.50/0082iVvEly8gacm42leeaj30jg0jgmyc.jpg?KID=imgbed,tva&Expires=1601179960&ssig=fwRq%2FWyfZS" |
| weibo_id        | 微博id            | str             | 'Jhv4a7KAd'                                                                                                                             |
| user_id         | 用户的id           | str             | '6004281123'                                                                                                                            |
| screen_name     | 用户名             | str             | '21世纪经济报道'                                                                                                                              |
| text            | 微博内容            | str             | '#新冠康复者二次...'                                                                                                                           |
| article_url     | 头条文章url         | str             | ""                                                                                                                                      |
| location        | 发布位置            | str             | ""                                                                                                                                      |
| at_users        | 艾特的用户，无艾特时为空列表  | [str, str, ...] | ['梨视频体育']                                                                                                                               |
| topics          | 话题，多个话题之间用','分隔 | str             | "迪丽热巴长歌行,迪丽热巴你是我的荣耀,迪丽热巴乔晶晶,星际领航员迪丽热巴"                                                                                                  |
| reposts_count   | 转发数             | str             | '65'                                                                                                                                    |
| comments_count  | 评论数             | str             | '33'                                                                                                                                    |
| attitudes_count | 点赞数             | str             | '14'                                                                                                                                    |
| created_at      | 创建时间            | str             | '2020-08-25 09:12'                                                                                                                      |
| source          | 发布工具            | str             | 'iPhone客户端'                                                                                                                             |
| pics            | 图片url           | str             | ''                                                                                                                                      |
| video_url       | 视频url           | str             | ''                                                                                                                                      |
| retweet         | 转发的微博相关信息       | dict            | 见下                                                                                                                                      |

+ 上面表格中`retweet`字段的值：

| key             | description     | value type                             | example                                                                                                                                  |
| --------------- | --------------- | -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| weibo_id        | 转发微博的id         | str                                    | "E46COzuWT"                                                                                                                              |
| user_id         | 用户的id           | str                                    | "1669879400"                                                                                                                             |
| screen_name     | 用户名             | str                                    | "Dear-迪丽热巴"                                                                                                                              |
| text            | 微博内容            | str                                    |                                                                                                                                          |
| article_url     | 头条文章的url        | str                                    | "..."                                                                                                                                    |
| location        | 发布位置，缺失时为空字符串   | str                                    |                                                                                                                                          |
| at_users        | 艾特的用户列表         | list                                   | ["Simple281314", "DILRABA的小宝贝儿绝不服输", "Dear-迪丽热巴"]                                                                                        |
| topics          | 话题，多个话题之间用','分隔 | "迪丽热巴长歌行,迪丽热巴你是我的荣耀,迪丽热巴乔晶晶,星际领航员迪丽热巴" |                                                                                                                                          |
| reposts_count   | 转发数量            | str                                    | "0"                                                                                                                                      |
| comments_count  | 评论数量            | str                                    | "0"                                                                                                                                      |
| attitudes_count | 点赞数量            | str                                    | "0"                                                                                                                                      |
| created_at      | 创建时间            | str                                    | "2016-08-18 11:36"                                                                                                                       |
| source          | 来源              | str                                    | "iPhone 6s Plus"                                                                                                                         |
| pics            | 图片              | list                                   | ["http://ww1.sinaimg.cn/large/63885668gw1f6xqh1wufxj21e00xc7wh.jpg", "http://ww2.sinaimg.cn/large/63885668gw1f6xqh598t3j21e00xc7wh.jpg"] |
| video_url       | 视频，无视频时为空字符串    | str                                    | ""                                                                                                                                       |

### 2. 推文展示接口

+ 根据推文id搜索推文
+ 路由： `/weibo_curl/api/statuses_show`

#### 请求参数

URL参数：

| key      | description                           | 是否必选       | example   |
| -------- | ------------------------------------- | ---------- | --------- |
| weibo_id | 微博id                                  | 是          | JmecdpWiO |
| cursor   | 查询第几页                                 | 否，默认第一页    | 2         |
| hot      | 表示获取热评还是获取普通评论，普通评论在第一页包含少数热评，其余为最新评论 | 否，默认获取普通评论 | 1         |

#### 返回格式

成功时返回json的 `result` 字段格式

| key           | value type                                           | description                                                      | example                                                                            |
| ------------- | ---------------------------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| original      | bool                                                 | 是否为原创                                                            | false                                                                              |
| weibo_id      | str                                                  | 微博id                                                             | "Jgs8rlEno"                                                                        |
| user_id       | str                                                  | 发布者的id                                                           | "1669879400"                                                                       |
| user_name     | str                                                  | 发布者的昵称                                                           | "Dear-迪丽热巴"                                                                        |
| video_url     | str                                                  | 视频的url                                                           | ""                                                                                 |
| original_pics | list                                                 | 原创图片的url                                                         |                                                                                    |
| retweet_pics  | list                                                 | 转发微博的图片url                                                       |                                                                                    |
| topics        | list                                                 | 微博中的话题                                                           | [""斯维诗越吃越美""]                                                                      |
| at_users      | list                                                 | 艾特的用户，每个元素是一个dict，其中包含"at_user_name"和"at_user_id"，分别表示艾特用户的名字和id | [{"at_user_name": "Swisse斯维诗", "at_user_id": "Swisse%E6%96%AF%E7%BB%B4%E8%AF%97"}] |
| weibo_content | 当original == true时该字段类型为str；当original == false时为dict | 微博内容，类型为str时即为微博原内容；当类型为dict时为转发微博的内容，具体字段见下面                    |                                                                                    |
| comments      | list                                                 | 评论列表，每个元素为一个dict，代表一条评论                                          |                                                                                    |
| max_page      | int                                                  | 评论的最大页数                                                          | 2000                                                                               |

当微博时转发类型时weibo_content为dict类型，其格式：

| key            | value type | description | example       |
| -------------- | ---------- | ----------- | ------------- |
| retweet        | str        | 转发内容        | "#中国首部海外...." |
| retweet_reason | str        | 转发理由        | "......"      |
| retweet_id     | str        | 所转发的微博的id   | "Jgoo94P6I"   |

comments中每个元素(dict)的格式，每个字段的值为null时表示未提取到该字段：

| key          | value type | description | example            |
| ------------ | ---------- | ----------- | ------------------ |
| is_hot       | bool       | 是否为热评       | true               |
| user_id      | str        | 评论用户id      | "1669879400"       |
| screen_name  | str        | 评论用户的用户名    | "Swisse斯维诗"        |
| content      | str        | 评论内容        | "..."              |
| like_num     | str        | 点赞数         | '616'              |
| publish_time | str        | 发布时间        | "2020-09-25 09:40" |
| publish_tool | str        | 发布工具        | "工具"               |

### 3. 用户搜索接口

+ 说明：根据关键词搜索用户
+ 路由：`/weibo_curl/api/users_search`

#### 请求参数

URL参数：

| key       | description                                         | 是否必选     | example |
| --------- | --------------------------------------------------- | -------- | ------- |
| keyword   | 搜索关键字                                               | 是        | 迪丽热巴    |
| cursor    | 查询第几页                                               | 否，默认第1页  | 2       |
| user_type | 查询限制的用户类型，值为1：机构认证， 2：个人认证，3：普通用户，其余值均为无限制          | 否，默认所有用户 | 1       |
| gender    | 查询限制性别，值为0：女性，值为1：男性，其余值均为无限制                       | 否，默认无限制  | 0       |
| age_limit | 查询年龄限制，值为1：低于18岁，2：19-22岁，3：30-39岁，4：超过40岁，其余值均为无限制 | 否，默认无限制  | 1       |

#### 返回格式

成功时返回json的 `result` 字段为一个l由多个dict组成的list，每个dict代表一个用户，每个元素(dict)的格式如下：(每个字段默认值均为None，表示未提取到项该信息)

| key             | description | value type           | example                                                   |
| --------------- | ----------- | -------------------- | --------------------------------------------------------- |
| user_id         | 用户的id       | str                  | '1669879400'                                              |
| head            | 用户头像        | str                  | "..."                                                     |
| nickname        | 昵称          | str                  | 'Dear-迪丽热巴'                                               |
| title           | 所拥有的的头衔     | str                  | '微博个人认证'                                                  |
| verified_reason | 认证原因        | str                  | '嘉行传媒签约演员\u3000'                                          |
| gender          | 性别          | int                  | 0                                                         |
| location        | 位置          | str                  | '上海 静安区'                                                  |
| description     | 简介          | str                  | '简介：一只喜欢默默表演的小透明。工作联系jaywalk@jaywalk.com.cn 🍒'           |
| tags            | 标签          | list，[str, str, ...] | ['迪丽热巴', 'Dilraba', '三生三世枕上书', '腾讯视频创造营', '电影日月', '声临其境'] |
| education       | 教育信息        | str                  | '教育信息：上海戏剧学院'                                             |
| work            | 工作信息        | str                  | '职业信息：嘉行传媒'                                               |
| weibo_num       | 微博数         | str                  | '1184'                                                    |
| following       | 关注数         | str                  | '257'                                                     |
| followers       | 粉丝数         | str                  | '7241万'                                                   |

注：

+ 当cursor超过50时会返回空result，cursor被置'0'

### 4. 用户展示接口

+ 说明：根据用户id搜索用户
+ 路由：`/weibo_curl/api/users_show`

#### 请求参数

URL查询字符串参数:

| key     | description | example      |
| ------- | ----------- | ------------ |
| user_id | 用户id        | '1669879400' |

#### 返回格式

成功时返回json的 `result` 字段格式： 

| key             | description | value type | example                |
| --------------- | ----------- | ---------- | ---------------------- |
| id              | 用户真实id      | str        | '1669879400'           |
| head            | 用户头像        | str        | "..."                  |
| nickname        | 昵称          | str        | 'Dear-迪丽热巴'            |
| gender          | 性别          | str        | '女'                    |
| location        | 用户所在地       | str        | '上海'                   |
| birthday        | 生日          | str        | '0001-00-00'           |
| description     | 用户简介        | str        | '一只喜欢默默表演的小透明。工作联系...' |
| verified_reason | 认证信息        | str        | '嘉行传媒签约演员'             |
| education       | 学习经历        | str        | '上海戏剧学院'               |
| work            | 工作经历        | str        | '嘉行传媒 '                |
| weibo_num       | 微博数         | int        | 1178                   |
| following       | 关注数         | int        | 257                    |
| followers       | 粉丝数         | int        | 72325060               |
| max_page        | 个人微博的最大页数   | int        | 200                    |

### 5. 用户时间线接口

+ 说明：根据用户id搜索用户的推文

+ 路由：`/weibo_curl/api/statuses_user_timeline`

#### 请求参数：

URL查询参数：

| key     | description                                   | 是否必选 | example      |
| ------- | --------------------------------------------- | ---- | ------------ |
| user_id | 用户id                                          | 是    | '1669879400' |
| cursor  | 指示本次查询的页数，默认为1                                | 否    | '2'          |
| filter  | 指示是否爬取转发微博，值为0时爬取全部微博（原创+转发），值为1是只爬取原创微博，默认为0 | 否    | 1            |

#### 返回格式

成功时返回`result`的格式：

| key              | description                                       | value type                                        | example                                                                                                                                                                                                        |
| ---------------- | ------------------------------------------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| weibo_id         | 微博id                                              | str                                               | 'Jgs8rlEno'                                                                                                                                                                                                    |
| user_id          | 用户id                                              | str                                               | '1669879400'                                                                                                                                                                                                   |
| text             | 微博内容                                              | str                                               | "..."                                                                                                                                                                                                          |
| article_url      | 头条文章url，没有时为空字符串                                  | str                                               | ''                                                                                                                                                                                                             |
| topics           | 微博设计的话题                                           | list，每个元素为一个str                                   | ["秋天的第一杯奶茶", "..."]                                                                                                                                                                                            |
| at_users         | @的用户                                              | list，每个元素为一个dict代表一个用户，包含`user_id`和`user_name`两个键 |                                                                                                                                                                                                                |
| pics             | 原创图片的url，每一个元素为一个图片                               | list                                              | ['http://ww1.sina...', '....']                                                                                                                                                                                 |
| retweet_pictures | 转发微博的图片url，每一个元素为一个图片                             | list                                              | ['....', '....']                                                                                                                                                                                               |
| original         | 是否为原创，true表示原创，即没有转发他人微博                          | bool                                              | true                                                                                                                                                                                                           |
| video_url        | 视频URL，没有时值为空串                                     | str                                               | "http://f.video.weibocdn.com/004CTge2gx07H4z7fXj201041200dmNl0E010.mp4?label=mp4_hd&template=852x480.25.0&trans_finger=62b30a3f061b162e421008955c73f536&Expires=1602637390&ssig=5znN56NTWR&KID=unistore,video" |
| location         | 微博发布位置，没有时为"无"                                    | str                                               |                                                                                                                                                                                                                |
| create_time      | 微博发布时间                                            | str                                               | '2020-08-13 17:14'                                                                                                                                                                                             |
| source           | 微博发布工具，没有时为"无"                                    | str                                               |                                                                                                                                                                                                                |
| attitudes_count  | 微博点赞数                                             | int                                               | 417438                                                                                                                                                                                                         |
| reposts_count    | 微博转发数                                             | int                                               | 6174                                                                                                                                                                                                           |
| comments_count   | 微博评论数                                             | int                                               | 22449                                                                                                                                                                                                          |
| retweet          | 所转发微博的内容，当没有转发微博时值为空字典，可以根据`original`字段判断是否有转发的微博 | dict                                              |                                                                                                                                                                                                                |

retweet字段的含义，其中信息均为所转发的微博的信息：

| key             | desciption | value type   | example                                                 |
| --------------- | ---------- | ------------ | ------------------------------------------------------- |
| weibo_id        | 微博的id      | str          | "Jn17oF5vN"                                             |
| user_id         | 用户的id      | str          | "1669879400"                                            |
| text            | 微博内容       | str          | "#我向祖国告白##祝福你中国#祝祖国生日快乐！今晚#央视国庆晚会# 见～ Dear-迪丽热巴的微博视频  " |
| article_url     | 微博文章的url   | ""           |                                                         |
| topics          | 微博中的话题     | list         | ["我向祖国告白", "祝福你中国", "央视国庆晚会"]                           |
| at_users        | @的用户       | list，内容同上个表格 |                                                         |
| attitudes_count | 点赞数量       | int          | 1167971                                                 |
| comments_count  | 评论数量       | int          | 204803                                                  |
| reposts_count   | 转发数量       | int          | 19219176                                                |
| pics            | 图片         | list         |                                                         |

### 6. 用户朋友列表接口（朋友关注的人）

+ 说明：根据用户的id搜索用户朋友，同时也要返回他们的信息
+ 路由：`/weibo_curl/api/friends_list`

#### 请求参数

URL参数：

| key     | description | 是否必选 | example    |
| ------- | ----------- | ---- | ---------- |
| user_id | 用户id        | 是    | 1669879400 |
| cursor  | 页数，默认第一页    | 否    | 1          |

#### 返回格式

成功时返回json的 `result` 字段格式：

| key          | value type | description             | example       |
| ------------ | ---------- | ----------------------- | ------------- |
| friend_list  | array      | 各朋友组成的列表，每个朋友被表示成一个dict | [{}, {}, ...] |
| max_page_num | int        | 最大页数                    | 10            |

friend_list中每个朋友所封装的dict格式：

| key       | value type | description | example      |
| --------- | ---------- | ----------- | ------------ |
| user_id   | str        | 用户的id       | "7482738083" |
| user_name | str        | 用户名         | "上海发布"       |
| fans_num  | int        | 粉丝数量        | 9332457      |

example:

```json
{
    "error_code": 0,
    "data": {
        "result": {
            "friend_list": [
                {
                    "user_id": "7482738083",
                    "user_name": "繁花BlossomsShanghai",
                    "fans_num": 11952
                },
                {
                    ......
                }
            ]
        },
        "cursor": 2
    },
    "error_msg": null
}
```

### 7. 用户粉丝列表接口

+ 说明：根据用户id搜索用户粉丝
+ 路由： `/weihbo_curl/api/followers_list`

#### 请求参数

URL参数：

| key     | description | 是否必选 | example    |
| ------- | ----------- | ---- | ---------- |
| user_id | 用户id        | 是    | 1669879400 |
| cursor  | 页数，默认第一页    | 否    | 1          |

#### 返回格式

成功时返回json的 `result` 字段格式：

| key           | value type | description             | example       |
| ------------- | ---------- | ----------------------- | ------------- |
| follower_list | array      | 各粉丝组成的列表，每个粉丝被表示成一个dict | [{}, {}, ...] |
| max_page_num  | int        | 最大页数                    | 10            |

followe_list中每个粉丝代表的dict的格式：

| key       | value type | description | example      |
| --------- | ---------- | ----------- | ------------ |
| user_id   | str        | 用户的id       | "6306674379" |
| user_name | str        | 用户名         | "胡小椒09"      |
| fans_num  | int        | 粉丝数量        | 8            |

example 与朋友列表接口返回的一样。

### 8. 账号设置接口

+ 请求方式：post

+ 路由： `\weibo_curl\api\update_account`

#### 请求的json格式

| key     | value type  | description             | example        |
| ------- | ----------- | ----------------------- | -------------- |
| cookies | list / null | 更新cookies的列表，为null表示不更新 | ['...', '...'] |
| proxies | list / null | 更新proxies的列表，为null表示不更新 | ['...', '...'] |

## 错误类型

```python
    # URL缺少参数
    URL_LACK_ARGS = {
        'error_code': 2001,
        'error_msg': 'URL is lack of arguments.'
    }

    # URL参数错误
    URL_ARGS_ERROR = {
        'error_code': 2002,
        'error_msg': 'URL args error.'
    }

    # 登录失效
    LOGIN_ERROR = {
        'error_code': 2003,
        'error-msg': 'An error occurred while logging in.'
    }

    # 用户不存在
    PAGE_NOT_FOUND = {
        'error_code': 2004,
        'error_msg': "Can't find the page."
    }

    # 微博网站返回其他错误信息
    ABNORMAL_HTTP_CODE = {
        'error_code': 2005,
        'error_msg': "Sina weibo return an abnormal http code."
    }

    # 未知错误
    UNKNOWN_ERROR = {
        'error_code': 2006,
        'error_msg': "An unknown error has occurred here."
    }

    # Cookie失效
    COOKIE_INVALID = {
        'error_code': 2007,
        'error_msg': "Cookie invalid."
    }

    # ip失效
    IP_INVALID = {
        'error_code': 2008,
        'error_msg': 'Current ip address invalid.'
    }
```

## 如何获取cookie

1.用Chrome打开<https://passport.weibo.cn/signin/login>；<br>
2.输入微博的用户名、密码，登录，如图所示：
![](https://picture.cognize.me/cognize/github/weibospider/cookie1.png)
登录成功后会跳转到<https://m.weibo.cn>;<br>
3.按F12键打开Chrome开发者工具，在地址栏输入并跳转到<https://weibo.cn>，跳转后会显示如下类似界面:
![](https://picture.cognize.me/cognize/github/weibospider/cookie2.png)
4.依此点击Chrome开发者工具中的Network->Name中的weibo.cn->Headers->Request Headers，"Cookie:"后的值即为我们要找的cookie值，复制即可，如图所示：
![](https://picture.cognize.me/cognize/github/weibospider/cookie3.png)
5.获得cookie后将其粘贴到account->account.json文件中的cookies对应配置项即可。