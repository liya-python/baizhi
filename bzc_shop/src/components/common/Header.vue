<template>
    <div class="header-box">
        <div class="header">
            <div class="content">
                <div class="logo full-left">
                    <router-link to="/"><img src="/static/image/logo.png" alt=""></router-link>
                </div>
                <ul class="nav full-left" >
                    <li v-for="(header,key) in header_list" :key="key">
                        <span v-if="header.is_site==0"><router-link :to="header.link">{{header.title}}</router-link></span>
                        <span v-if="header.is_site==1"><a :href="header.link">{{header.title}}</a></span>

                    </li>
                </ul>
                <!--         登录之后展示的       -->
                <div class="login-bar full-right" v-if="token">

                    <div class="shop-cart full-left">
                        <img src="/static/image/cart.svg" alt="">
                        <span><router-link to="/cart">
                            {{this.$store.state.cart_length}}购物车</router-link></span>
                    </div>
                    <div class="login-box full-left">
                        <router-link to="//order/list">个人中心</router-link>
                        &nbsp;|&nbsp;
                        <a href="javascript:;" @click="exit">退出登录</a>
                    </div>
                </div>
                <!--        登录之前的        -->
                <div class="login-bar full-right" v-else>
                    <div class="shop-cart full-left">
                        <img src="/static/image/cart.svg" alt="">
                        <span><router-link to="/cart">购物车</router-link></span>
                    </div>
                    <div class="login-box full-left">
                        <router-link to="/login">登录</router-link>
                        &nbsp;|&nbsp;
                        <router-link to="/register">注册</router-link>
<!--                        <span>注册</span>-->
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Header",
        // props:['cart_length'],
        data(){
            return {
                header_list:[],
                token: "",
                cart_length:0,
            }
        },
        methods:{
            get_user() {
                // console.log(sessionStorage.token1,'1111');
                this.token = localStorage.token || sessionStorage.token;
                // console.log(this.token)
            },
            exit(){
              localStorage.removeItem('token');
              // this.token = 0;
              this.$router.go(0);
            },
            get_all_header(){
                this.$axios({
                    url:'http://127.0.0.1:9000/home/nav/',
                    method:'get',
                }).then(res =>{
                    // console.log(res);
                    for (let ress of res.data){
                        // console.log(ress);
                        if (ress.position ===1){
                            this.header_list.unshift(ress)
                        }
                    }
                    // console.log(this.header_list);

                })
            }
        },
        created() {
            // console.log(this.$store.state.cart_length,'11111');
            // this.cart_length=this.$store.state.cart_length
            // 在页面加载之前判断是否有登录信息
            this.get_user();
            this.get_all_header()
        },
    }
</script>

<style scoped>
    .header-box {
        height: 80px;
    }

    .header {
        width: 100%;
        height: 80px;
        box-shadow: 0 0.5px 0.5px 0 #c9c9c9;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        margin: auto;
        z-index: 99;
        background: #fff;
    }

    .header .content {
        max-width: 1200px;
        width: 100%;
        margin: 0 auto;
    }

    .header .content .logo {
        height: 80px;
        line-height: 80px;
        margin-right: 50px;
        cursor: pointer; /* 设置光标的形状为爪子 */
    }

    .header .content .logo img {
        vertical-align: middle;
    }

    .header .nav li {
        float: left;
        height: 80px;
        line-height: 80px;
        margin-right: 30px;
        font-size: 30px;
        color: #4a4a4a;
        cursor: pointer;
    }

    .header .nav li span {
        padding-bottom: 16px;
        padding-left: 5px;
        padding-right: 5px;
    }

    .header .nav li span a {
        display: inline-block;
    }

    .header .nav li .this {
        color: #4a4a4a;
        border-bottom: 4px solid #ffc210;
    }

    .header .nav li:hover span {
        color: #000;
    }

    .header .login-bar {
        height: 80px;
    }

    .header .login-bar .shop-cart {
        margin-right: 20px;
        border-radius: 17px;
        background: #f7f7f7;
        cursor: pointer;
        font-size: 14px;
        height: 28px;
        width: 100px;
        margin-top: 30px;
        line-height: 32px;
        text-align: center;
    }

    .header .login-bar .shop-cart:hover {
        background: #f0f0f0;
    }

    .header .login-bar .shop-cart img {
        width: 15px;
        margin-right: 4px;
        margin-left: 6px;
    }

    .header .login-bar .shop-cart span {
        margin-right: 6px;
    }

    .header .login-bar .login-box {
        margin-top: 33px;
    }

    .header .login-bar .login-box span {
        color: #4a4a4a;
        cursor: pointer;
    }

    .header .login-bar .login-box span:hover {
        color: #000000;
    }

    a {
        text-decoration: none;
        color: #333;
    }

    .member {
        display: inline-block;
        height: 34px;
        margin-left: 20px;
    }

    .member img {
        width: 26px;
        height: 26px;
        border-radius: 50%;
        display: inline-block;
    }

    .member img:hover {
        border: 1px solid yellow;
    }

    .header .login-bar .login-box1 {
        margin-top: 16px;
    }

    a:hover {
        display: inline-block;
    }
</style>
