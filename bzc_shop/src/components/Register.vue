<template>
    <div class="box">
        <img src="../../static/image/1111.jpg" alt="">
        <div class="register">
            <div class="register_box">
                <div class="register-title">百知教育在线平台注册</div>
                <div class="inp">
                    <input v-model="phone" type="text" placeholder="手机号码" class="user" @blur="check_phone">
                    <input v-model="password" type="password" placeholder="注册密码" class="user" @blur="check_pwd">
                    <div id="geetest"></div>
                    <div class="sms-box">
                        <input v-model="code" type="text" maxlength="6" placeholder="输入验证码" class="user">
                        <div class="sms-btn"  v-show="show" @click="send_msg">获取验证码</div>
                        <div class="sms-btn"  v-show="!show" @click="send_msg">{{sms_text}}秒后可重新获取</div>

                    </div>
                    <button class="register_btn" @click="register_user">注册</button>
                    <p class="go_login">已有账号
                        <router-link to="/login">直接登录</router-link>
<!--                        <span>直接登录</span>-->
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Register",
        data(){
            return {
                phone:'',
                password:'',
                code:'',
                flag:0,
                timer:null,
                sms_text:'',
                show:true,
            }
        },
        methods:{
            send_msg(){
                // console.log(this.flag)
                if(this.flag){
                    let self = this;
                    this.$axios({
                        url: "http://127.0.0.1:9000/user/sms/",
                        method: "get",
                        params: {
                            phone: this.phone,
                        }
                    }).then(response => {
                        console.log(response);
                        self.time()
                        // 成功提示
                        this.$message.success({
                            message: '短信已经发送到手机，请注意查收',
                            type: 'success',
                            showClose: true,
                            duration: 1000,
                        })

                    }).catch(error => {
                        console.log(error);
                        this.$message.error("当前手机号已经发送过短信")
                    })
                }
                //     this.$message.error('手机号格式有误或已被注册')
                // }
            },
            time(){
                const TIME_COUNT = 60;
                if (!this.timer) {
                    this.sms_text = TIME_COUNT;
                    this.show = false;
                    this.timer = setInterval(() => {
                        if (this.sms_text > 0 && this.sms_text <= TIME_COUNT) {
                            this.sms_text--;
                        } else {
                            this.show = true;
                            clearInterval(this.timer);
                            this.timer = null;
                        }
                    }, 1000)
                }

            },
            check_phone(){
                let pattern = /^1[3-9]\d{9}$/
                if (pattern.test(this.phone)){
                    // alert('匹配成功')
                    this.$axios({
                        url:'http://127.0.0.1:9000/user/phone/',
                        method: 'get',
                        params:{
                            phone: this.phone
                        }
                    }).then(response =>{
                        this.$message.success('手机号可用')
                        this.flag = 1
                    }).catch(error =>{
                        console.log(error)
                        this.$message.error('手机号已被注册')
                    })

                }else{
                    this.$message.error('手机号码不合法')
                }
            },
            check_pwd(){
                let pattern = /^\w{3,18}$/
                if (pattern.test(this.password)){
                    this.$message({
                        message: '密码输入合法',
                        type: 'success',
                        showClose: true,
                        duration: 1000,
                    })
                }else{
                    this.$message.error('密码应由3-18位数字、下划线或字母组成')
                }
            },
            register_user(){
                this.$axios({
                    url: 'http://127.0.0.1:9000/user/users/',
                    method: 'post',
                    data: {
                        phone:this.phone,
                        password:this.password,
                        code:this.code,
                    }
                }).then(response =>{
                    console.log(response);
                    localStorage.setItem('token',response.data.token)
                    let self = this;
                    this.$alert("注册成功", "百知教育欢迎你", {
                        callback() {
                            self.$router.push("/");
                        }
                    })

                }).catch(error =>{
                    console.log(error);
                })
            }
        }
    }
</script>

<style scoped>
    .box {
        width: 100%;
        height: 100%;
        position: relative;
        overflow: hidden;
    }

    .box img {
        width: 100%;
        min-height: 100%;
    }

    .box .register {
        position: absolute;
        width: 500px;
        height: 400px;
        top: 0;
        left: 0;
        margin: auto;
        right: 0;
        bottom: 0;
        top: -338px;
    }

    .register .register-title {
        width: 100%;
        font-size: 24px;
        text-align: center;
        padding-top: 30px;
        padding-bottom: 30px;
        color: #4a4a4a;
        letter-spacing: .39px;
    }

    .register-title img {
        width: 190px;
        height: auto;
    }

    .register-title p {
        font-family: PingFangSC-Regular;
        font-size: 18px;
        color: #fff;
        letter-spacing: .29px;
        padding-top: 10px;
        padding-bottom: 50px;
    }

    .register_box {
        width: 400px;
        height: auto;
        background: #fff;
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
        border-radius: 4px;
        margin: 0 auto;
        padding-bottom: 40px;
    }

    .register_box .title {
        font-size: 20px;
        color: #9b9b9b;
        letter-spacing: .32px;
        border-bottom: 1px solid #e6e6e6;
        display: flex;
        justify-content: space-around;
        padding: 50px 60px 0 60px;
        margin-bottom: 20px;
        cursor: pointer;
    }

    .register_box .title span:nth-of-type(1) {
        color: #4a4a4a;
        border-bottom: 2px solid #84cc39;
    }

    .inp {
        width: 350px;
        margin: 0 auto;
    }

    .inp input {
        border: 0;
        outline: 0;
        width: 100%;
        height: 45px;
        border-radius: 4px;
        border: 1px solid #d9d9d9;
        text-indent: 20px;
        font-size: 14px;
        background: #fff !important;
    }

    .inp input.user {
        margin-bottom: 16px;
    }

    .inp .rember {
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        margin-top: 10px;
    }

    .inp .rember p:first-of-type {
        font-size: 12px;
        color: #4a4a4a;
        letter-spacing: .19px;
        margin-left: 22px;
        display: -ms-flexbox;
        display: flex;
        -ms-flex-align: center;
        align-items: center;
        /*position: relative;*/
    }

    .inp .rember p:nth-of-type(2) {
        font-size: 14px;
        color: #9b9b9b;
        letter-spacing: .19px;
        cursor: pointer;
    }

    .inp .rember input {
        outline: 0;
        width: 30px;
        height: 45px;
        border-radius: 4px;
        border: 1px solid #d9d9d9;
        text-indent: 20px;
        font-size: 14px;
        background: #fff !important;
    }

    .inp .rember p span {
        display: inline-block;
        font-size: 12px;
        width: 100px;
        /*position: absolute;*/
        /*left: 20px;*/

    }

    #geetest {
        margin-top: 20px;
    }

    .register_btn {
        width: 100%;
        height: 45px;
        background: #84cc39;
        border-radius: 5px;
        font-size: 16px;
        color: #fff;
        letter-spacing: .26px;
        margin-top: 30px;
    }

    .inp .go_login {
        text-align: center;
        font-size: 14px;
        color: #9b9b9b;
        letter-spacing: .26px;
        padding-top: 20px;
    }

    .inp .go_login span {
        color: #84cc39;
        cursor: pointer;
    }

    .sms-box {
        position: relative;
    }

    .sms-btn {
        font-size: 14px;
        color: #ffc210;
        letter-spacing: .26px;
        position: absolute;
        right: 16px;
        top: 10px;
        cursor: pointer;
        overflow: hidden;
        background: #fff;
        border-left: 1px solid #484848;
        padding-left: 16px;
        padding-bottom: 4px;
    }
</style>
