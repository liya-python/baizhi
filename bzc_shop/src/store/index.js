import Vue from 'vue'

import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        // 共享的数据
        cart_length:0,
    },
    mutations:{
        // 检测提交的动作
        add_cart(state, data){
            state.cart_length = data;
        }
    },
})
