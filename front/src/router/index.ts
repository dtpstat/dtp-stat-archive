import Vue from 'vue';
import Router from 'vue-router';
import DTPArea from "@/views/dtp-area/DTPArea";
import DTPIndex from "@/views/dtp-index/DTPIndex";
import About from "@/views/About.vue";


Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'Index',
            component: DTPIndex
        },
        {
            path: '/area',
            name: 'Area',
            component: DTPArea
        },
        {
            path: '/about',
            name: 'About',
            component: About
        }
    ]
})