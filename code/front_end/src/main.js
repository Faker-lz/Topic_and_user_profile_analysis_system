import Vue from 'vue'
import App from './App.vue'
//引入axios
import axios from 'axios'
//引入router配置
import router from './router'
import VueRouter from 'vue-router';
//引入icon字体配置文件
import './assets/icon/iconfont.js';
// 引入 echarts 核心模块，核心模块提供了 echarts 使用必须要的接口。
import * as echarts from 'echarts';
import 'echarts-wordcloud';
//引入animate动画库
import "animate.css"
//引入字体
import 'font-awesome/css/font-awesome.min.css'
//引入element-ui组件库
import './plugins/element.js'

// 将echarts保存为全局变量
Vue.prototype.$echarts = echarts;

Vue.config.productionTip = false
Vue.prototype.$axios = axios
//axios全局配置
axios.defaults.baseURL = 'http://127.0.0.1:81/api/tag/'
Vue.use(VueRouter)

//设置路由跳转时把页面的title改变
router.beforeEach((to, from, next) => {
  if (to.meta.title) { //路由发生变化时候修改页面中的title
    document.title = to.meta.title
  }
  next()
})
// router.beforeEach((to, from, next) => {
//   if (to.name !== 'login' && window.localStorage.getItem('token') == undefined) {
//     // 不存在
//     next({ name: 'login' })
//   } else {
//     // 存在就放行
//     next()
//   }
// })

new Vue({
  el: '#app',
  render: h => h(App),
  router,
  beforeCreate() {
    Vue.prototype.$bus = this //安装全局事件总线
  },
})