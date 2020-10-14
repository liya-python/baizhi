<template>
    <div class="success">
        <Header/>
        <div class="main">
            <div class="title">
                <div class="success-tips">
                    <p class="tips1">您已成功购买 {{course_list.length}} 门课程！</p>
                    <p class="tips2">你还可以加入QQ群 <span>11111111</span> 学习交流</p>
                </div>
            </div>
            <div class="order-info">
                <p class="info1"><b>付款时间：</b><span>{{pay_time}}</span></p>
                <p class="info2"><b>付款金额：</b><span>￥{{total_price}}元</span></p>
                <p class="info3"><b>课程信息：</b></p>
                <ul class="nav">
                    <li class="order-info">订单</li>
                    <li class="course-expire">有效期</li>
                    <li class="course-expire">到期时间</li>
                    <li class="course-price">课程价格</li>
                    <li class="real-price">实付金额</li>
                    <li class="order-status">交易状态</li>
                    <li class="order-do">交易操作</li>
                </ul>
                <ul class="nav user-data-list" v-for="course in course_list">
                    <li class="order-info">
                        <img :src="course.course_img" alt="">
                        <div class="order-info-title">
                            <p class="course-title">{{course.name}}</p>
                            <p class="price-service">{{course.discount_name}}</p>
                        </div>
                    </li>
                    <li class="course-expire">{{course.expire_text}}</li>
                    <li class="course-expire">{{course.end_time}}</li>
                    <li class="course-expire">{{course.origin_price}}</li>
                    <li class="real-price">{{course.real_price}}</li>
                    <li class="order-status">交易成功</li>
                    <li class="order-do">
                        <span class="btn btn2">去学习</span>
                    </li>
                </ul>
            </div>
            <div class="wechat-code">
            </div>
<!--            <div class="study">-->
<!--                可去我的订单查看<span><rourer-link to=""></rourer-link></span>-->
<!--            </div>-->
        </div>
        <Footer/>
    </div>
</template>

<script>
    import Footer from "./common/Footer";
    import Header from "./common/Header";
    export default {
        name: "OrderSuccess",
        data(){
            return {
                course_list:[],
                total_price:0,
                pay_time:0,
            }
        },
        methods: {
            get_time(times){
                // console.log(times)
                let time = new Date(times)
                let year = time.getFullYear();
                // console.log(year)
                let month =time.getMonth()+1;
                month = (month<10)?'0'+month:month;
                let day = time.getDate();
                day = (day<10)? '0'+day:day;
                console.log(day);
                let hour = (time.getHours()<10)?'0'+(time.getHours()):(time.getHours());
                let minu = (time.getMinutes()<10)? '0'+(time.getMinutes()):(time.getMinutes());
                let to = year + "-" + (month) + "-" + (day) +'  '+hour+':'+minu+':00';
                this.pay_time = to;
            },
            // 检查用户是否已经登录
            check_user_login() {
                let token = localStorage.token || sessionStorage.token;
                if (!token) {
                    let self = this;
                    this.$confirm("对不起，请登录后再继续支付", {
                        callback() {
                            self.$router.push("/login");
                        }
                    });
                    return false
                }
                return token;
            },
            // 携带参数发送到后台  验证支付结果

            AliPayResult() {
                let token = this.check_user_login();
                // console.log(location.search);
                this.$axios.get( "http://127.0.0.1:9000/payment/result/" + location.search,{
                    headers:{
                        // 提交购物车时必须携带token  jwt 后必须跟空格
                        "Authorization": "jwt " + token,
                    }
                }).then(res => {
                    console.log(res.data);
                    this.course_list = res.data.course_list;
                    this.total_price= res.data.total_price;
                    let pay_time =res.data.pay_time;
                    this.get_time(pay_time)
                    // let time = new Date(times)
                    this.$message.success(res.data.message)
                }).catch(error => {
                    this.$message.success(error.message);
                })
            },
        },
        created() {
            this.AliPayResult();
        },
        components: {
            Footer, Header
        }
    }
</script>

<style scoped>
    .success {
        padding-top: 80px;
    }

    .main {
        height: 100%;
        padding-top: 25px;
        padding-bottom: 25px;
        margin: 0 auto;
        width: 1200px;
        background: #fff;
    }

    .main .title {
        display: flex;
        -ms-flex-align: center;
        align-items: center;
        padding: 25px 40px;
        border-bottom: 1px solid #f2f2f2;
    }

    .main .title .success-tips {
        box-sizing: border-box;
    }

    .title img {
        vertical-align: middle;
        width: 60px;
        height: 60px;
        margin-right: 40px;
    }

    .title .success-tips {
        box-sizing: border-box;
    }

    .title .tips1 {
        font-size: 22px;
        color: #000;
    }

    .title .tips2 {
        font-size: 16px;
        color: #4a4a4a;
        letter-spacing: 0;
        text-align: center;
        margin-top: 10px;
    }

    .title .tips2 span {
        color: #ec6730;
    }

    .order-info1 {
        padding: 25px 48px;
        padding-bottom: 15px;
        border-bottom: 1px solid #f2f2f2;
    }

    .order-info p {
        display: -ms-flexbox;
        display: flex;
        margin-bottom: 10px;
        font-size: 16px;
    }

    .order-info p b {
        font-weight: 400;
        color: #9d9d9d;
        white-space: nowrap;
    }

    .wechat-code {
        display: flex;
        -ms-flex-align: center;
        align-items: center;
        padding: 25px 40px;
        border-bottom: 1px solid #f2f2f2;
    }

    .wechat-code > img {
        width: 100px;
        height: 100px;
        margin-right: 15px;
    }

    .wechat-code p {
        font-size: 14px;
        color: #d0021b;
        display: -ms-flexbox;
        display: flex;
        -ms-flex-align: center;
        align-items: center;
    }

    .wechat-code p > img {
        width: 16px;
        height: 16px;
        margin-right: 10px;
    }

    .study {
        padding: 25px 40px;
    }

    .study span {
        display: block;
        width: 140px;
        height: 42px;
        text-align: center;
        line-height: 42px;
        cursor: pointer;
        background: #ffc210;
        border-radius: 6px;
        font-size: 16px;
        color: #fff;
    }





    .main .banner {
        width: 100%;
        height: 324px;
        /*background: url(../../static/image/r9RW20TrQ0Y.jpg) no-repeat;*/
        background-size: cover;
        z-index: 1;
    }

    /*.profile {*/
    /*    width: 1200px;*/
    /*    margin: 0 auto;*/
    /*}*/

    /*.profile-info {*/
    /*    text-align: center;*/
    /*    margin-top: -80px;*/
    /*}*/

    /*.avatar {*/
    /*    width: 120px;*/
    /*    height: 120px;*/
    /*    border-radius: 60px;*/
    /*    overflow: hidden;*/
    /*    margin: 0 auto;*/
    /*}*/

    /*.user-name {*/
    /*    display: block;*/
    /*    font-size: 24px;*/
    /*    color: #4a4a4a;*/
    /*    margin-top: 14px;*/
    /*}*/

    /*.user-job {*/
    /*    display: block;*/
    /*    font-size: 11px;*/
    /*    color: #9b9b9b;*/
    /*}*/

    /*.my-item {*/
    /*    list-style: none;*/
    /*    line-height: 1.42857143;*/
    /*    color: #333;*/
    /*    width: 474px;*/
    /*    height: 31px;*/
    /*    display: -ms-flexbox;*/
    /*    display: flex;*/
    /*    cursor: pointer;*/
    /*    margin: 41px auto 0;*/
    /*    -ms-flex-pack: justify;*/
    /*    justify-content: space-between;*/
    /*}*/

    .my-item .active {
        border-bottom: 1px solid #000;
    }

    /*.user-data {*/
    /*    width: 1200px;*/
    /*    height: auto;*/
    /*    margin: 0 auto;*/
    /*    padding-top: 30px;*/
    /*    border-top: 1px solid #e8e8e8;*/
    /*    margin-bottom: 63px;*/
    /*}*/
    .nav {
        width: 100%;
        height: 60px;
        background: #e9e9e9;
        display: -ms-flexbox;
        display: flex;
        -ms-flex-align: center;
        align-items: center;
    }

    .nav li {
        margin-left: 20px;
        margin-right: 28px;
        height: 60px;
        line-height: 60px;
        list-style: none;
        font-size: 13px;
        color: #333;
        border-bottom: 1px solid #e9e9e9;
        width: 160px;
    }

    .nav .order-info {
        width: 325px;
    }

    .nav .course-expire {
        width: 180px;
    }

    .nav .course-price {
        width: 130px;
    }

    /*.user-data-header {*/
    /*    display: flex;*/
    /*    height: 44px;*/
    /*    color: #4a4a4a;*/
    /*    font-size: 14px;*/
    /*    background: #f3f3f3;*/
    /*    -ms-flex-align: center;*/
    /*    align-items: center;*/
    /*}*/

    /*.order-time {*/
    /*    font-size: 12px;*/
    /*    display: inline-block;*/
    /*    margin-left: 20px;*/
    /*}*/

    /*.order-num {*/
    /*    font-size: 12px;*/
    /*    display: inline-block;*/
    /*    margin-left: 29px;*/
    /*}*/

    .user-data-list {
        height: 100%;
        display: flex;
    }

    .user-data-list {
        background: none;
    }

    .user-data-list li {
        height: 60px;
        line-height: 60px;
    }

    .user-data-list .order-info {
        display: flex;
        align-items: center;
        margin-right: 28px;
    }

    .user-data-list .order-info img {
        max-width: 100px;
        max-height: 75px;
        margin-right: 22px;
    }

    .course-title {
        width: 203px;
        font-size: 13px;
        color: #333;
        line-height: 20px;
        margin-top: -10px;
    }

    .order-info-title .price-service {
        line-height: 18px;
    }

    .price-service {
        font-size: 12px;
        color: #fa6240;
        padding: 0 5px;
        border: 1px solid #fa6240;
        border-radius: 4px;
        margin-top: 4px;
        position: absolute;
    }

    .order-info-title {
        margin-top: -10px;
    }

    .user-data-list .course-expire {
        font-size: 12px;
        color: #ff5502;
        width: 200px;
        text-align: center;
    }

    .btn {
        width: 100px;
        height: 32px;
        font-size: 14px;
        color: #fff;
        background: #ffc210;
        border-radius: 4px;
        border: none;
        outline: none;
        transition: all .25s ease;
        display: inline-block;
        line-height: 32px;
        text-align: center;
        cursor: pointer;
    }
</style>
