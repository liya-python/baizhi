import Vue from 'vue'
import Router from 'vue-router'
import Index from "../components/Index";
import Login from "../components/Login";
import Register from "../components/Register";
import Course from "../components/Course";
import CourseDetail from "../components/CourseDetail";
import Cart from "../components/Cart";
import Order from "../components/Order";
import OrderSuccess from "../components/OrderSuccess";
import OrderList from "../components/OrderList";


Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path:'/',
            component:Index,
        },
        {
            path: '/index',
            name:Index,
            component: Index,
        },
        {
            path: '/login',
            name: Login,
            component: Login,
        },
        {
            path: '/register',
            name: Register,
            component: Register,
        },
        {
            path: '/course',
            name: Course,
            component: Course,
        },
        {
            path: '/detail/:id',
            name: CourseDetail,
            component: CourseDetail,
        },
        {
            path: '/cart',
            name: Cart,
            component: Cart,
        },
        {
            path: '/order',
            name: Order,
            component: Order,
        },
        {
            path: '/payments/result',
            name: OrderSuccess,
            component: OrderSuccess,
        },
        {path: "/order/list", component: OrderList},
    ]
})
