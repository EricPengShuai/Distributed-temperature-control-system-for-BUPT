import Vue from 'vue'
import App from "./App.vue";
import router from './router'
import store from './store';
import io from 'socket.io-client';
import VueSocketIOExd from 'vue-socket.io-extended';
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.use(VueSocketIOExd, io('http://localhost:5000'), { store })

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app')

