import Vue from 'vue';
import Router from 'vue-router';
import DArea from "@/views/d-area/DArea";
import DIndex from "@/views/d-index/DIndex";
import About from "@/views/About.vue";


Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'Index',
            component: DIndex
        },
        {
            path: '/area',
            name: 'Area',
            component: DArea
        },
        {
            path: '/about',
            name: 'About',
            component: About
        }
    ]
})