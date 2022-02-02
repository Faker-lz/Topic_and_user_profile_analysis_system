import VueRouter from 'vue-router'

import wbAnalyze from '../pages/wbAnalyze';
import home from '../pages/home';
import login from '../pages/login';
import blog_detail from '../pages/blog_detail';
import person_list from '../pages/person_list';

export default new VueRouter({
    routes: [{
            path: "/",
            component: home,
            meta: {
                title: "舆情系统"
            }
        },
        {
            path: "/home",
            component: home,
            meta: {
                title: "舆情系统"
            }
        },
        {
            path: "/wb",
            component: wbAnalyze,
            meta: {
                title: "微博舆情分析"
            }
        },
        {
            path: "/login",
            name: 'login',
            component: login,
            meta: {
                title: "登录注册"
            }
        },
        {
            path: "/blog_detail",
            component: blog_detail,
            meta: {
                title: "博文详情"
            }
        },
        {
            path: "/person_list",
            component: person_list,
            meta: {
                title: "用户列表"
            }
        }
    ],
    mode: "history"
})