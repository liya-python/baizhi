// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from "axios"
import ElementUI from 'element-ui'
import "element-ui/lib/theme-chalk/index.css"
// 导入全局的css配置
import "../static/css/global.css"
import '../static/js/gt'
import VideoPlayer from 'vue-video-player'
require('video.js/dist/video-js.css')
require('vue-video-player/src/custom-theme.css')
Vue.use(VideoPlayer)
// 将axios注入到Vue的实例中
Vue.prototype.$axios = axios

Vue.use(ElementUI)


Vue.config.productionTip = false
import store from './store/index'

/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    store,
    components: {App},
    template: '<App/>',
    // this.axios.interceptors.response.use(response => {
    //     if (response) {
    //         switch (response.data.code) {
    //             case 403: //与后台约定登录失效的返回码,根据实际情况处理
    //                 localStorage.clear();     //删除用户信息
    //                 //如果超时就处理 ，指定要跳转的页面(比如登陆页)
    //                 Message({
    //                     message: 'token失效,请重新登录!',
    //                     type: 'warning',
    //                     center: true,
    //                     onClose:function () {
    //                         console.log('关闭了看下')
    //                         router.replace({
    //                             path: '/user/login',
    //                         })
    //                     }
    //                 });
    //         }
    //     }
    //     return response;
    // }, error => {
    //     return Promise.reject(error.response.data) //返回接口返回的错误信息
    // })
})
