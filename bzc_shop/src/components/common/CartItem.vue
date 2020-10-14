<template>
    <div class="cart_item">
        <div class="cart_column column_1">
            <el-checkbox class="my_el_checkbox" v-model="course.selected"></el-checkbox>
        </div>
        <div class="cart_column column_2">
            <img :src="course.course_img" alt="">
            <span><router-link :to="'/detail/'+course.id">{{course.name}}</router-link></span>
        </div>
        <div class="cart_column column_3">
            <el-select v-model="course.expire_id" size="mini" placeholder="请选择购买有效期" class="my_el_select">
                <el-option :label="item.expire_text" :value="item.id" :key="item.id"
                           v-for="item in course.expire_list"></el-option>
            </el-select>
        </div>
        <div class="cart_column column_4">¥{{course.price}}</div>
        <div class="cart_column column_4" @click="del_cart(course.id)">删除</div>
    </div>
</template>

<script>
    export default {
        name: "CartItem",
        props: ['course','check'],
        data() {
            return {
                expire: 0,
                checked: '',
                price:'',
            }
        },
        methods: {
            change_expire() {
                let token = sessionStorage.token || localStorage.token;
                this.$axios.put( "http://127.0.0.1:9000/cart/option/", {
                    course_id: this.course.id,
                    expire_id: this.course.expire_id,
                }, {
                    headers: {
                        // 提交购物车时必须携带token  jwt 后必须跟空格
                        "Authorization": "jwt " + token,
                    }
                }).then(response=>{
                    // console.log(response.data);
                    // 改变价格
                    this.course.price = response.data.price
                    // this.$emit('')
                    this.$message({
                        message: '恭喜你，改变有效期时间成功',
                        type: 'success',
                        showClose: true,
                        duration: 1000,
                    })
                    this.$emit("change_select");
                }).catch(error=>{
                    console.log(error);
                    if (error.response.status===401){
                        let self = this;
                        this.$confirm("对不起，用户信息失效，请登录", {
                            callback() {
                                self.$router.push("/login");
                            }
                        });
                    }else{
                        this.$message.error(error.message);
                    }
                })
            },
            // 状态切换
            change_select() {
                let token = localStorage.token || sessionStorage.token;
                this.$axios.patch('http://127.0.0.1:9000/cart/option/', {
                    selected: this.course.selected,
                    course_id: this.course.id,
                }, {
                    headers: {
                        // 提交token必须在请求头声明token  jwt必须有空格
                        "Authorization": "jwt " + token,
                    }
                }).then(response => {
                    this.$message.success(response.data.message);

                    // 向父组件提交事件 来修改购物车已勾选的课程的总价
                    this.$emit("change_select");

                }).catch(error => {
                    console.log(error);
                    // this.$message.error(error.response)
                    if (error.response.status===401){
                        let self = this;
                        this.$confirm("对不起，用户信息失效，请登录", {
                            callback() {
                                self.$router.push("/login");
                            }
                        });
                    }else{
                        this.$message.error(error.message);
                    }
                })
            },
            del_cart(id) {
                console.log(id);
                let token = localStorage.token || sessionStorage.token;
                this.$axios({
                    url: 'http://127.0.0.1:9000/cart/option/',
                    method: 'delete',
                    params: {
                        id: id,
                    },
                    headers: {
                        "Authorization": "jwt " + token,
                    }
                }).then(response => {
                    console.log(response.data)
                    this.$message({
                        message: '恭喜你，删除成功',
                        type: 'success',
                        showClose: true,
                        duration: 1000,
                    })
                    // 当自组价删除商品时需要通知父组件来执行对应的方法  可以向父组件提交事件
                    this.$emit("del_course");
                }).catch(error =>{
                    console.log(error);
                    if (error.response.status===401){
                        let self = this;
                        this.$confirm("对不起，用户信息失效，请登录", {
                            callback() {
                                self.$router.push("/login");
                            }
                        });
                    }else{
                        this.$message.error(error.message);
                    }
                })
            }

        },
        watch:{
            check(){
                if (this.check===true){
                    this.course.selected=true;
                    console.log(this.course.selected);
                    // this.checked();
                }else{
                    this.course.selected=false;
                    console.log(this.course.selected);
                    // this.checked();
                }
            },
            // 通过监测课程id来切换有效期
            'course.expire_id': function () {
                // 后台发送请求切换状态
                this.change_expire();
            },
            // 通过监测select的变化来改变当前的选中状态
            'course.selected': function () {
                // 后台发送请求切换状态
                this.change_select()
            },
        },
        created() {
            this.checked = this.course.selected
            // console.log(this.checked);

        },
    }



</script>

<style scoped>
    .cart_item::after {
        content: "";
        display: block;
        clear: both;
    }

    .cart_column {
        float: left;
        height: 250px;
    }

    .cart_item .column_1 {
        width: 88px;
        position: relative;
    }

    .my_el_checkbox {
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        top: 0;
        /*color: yellow;*/
        margin: auto;
        width: 16px;
        height: 16px;
    }

    .cart_item .column_2 {
        padding: 67px 10px;
        width: 520px;
        height: 116px;
    }

    .cart_item .column_2 img {
        width: 175px;
        height: 115px;
        margin-right: 35px;
        vertical-align: middle;
    }

    .cart_item .column_3 {
        width: 197px;
        position: relative;
        padding-left: 10px;
    }

    .my_el_select {
        width: 117px;
        height: 28px;
        position: absolute;
        top: 0;
        bottom: 0;
        margin: auto;
    }

    .cart_item .column_4 {
        padding: 67px 10px;
        height: 116px;
        width: 142px;
        line-height: 116px;
    }

</style>
