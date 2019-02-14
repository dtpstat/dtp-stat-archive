import Vue from 'vue'

import router from './router'
import store from './store'

import App from '@/app/App'

Vue.config.productionTip = false

class AppCore {
  private instance!: Vue;

  private init() {
    this.instance = new Vue({
      router,
      store,
      render: h => h(App),
    }).$mount('#app')

  }

  constructor() {
    this.init();
  }
}

new AppCore();