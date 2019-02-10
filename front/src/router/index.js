import Vue from 'vue'
import Router from 'vue-router'
import Index from "@/views/Index";
import About from "@/views/About";
import Area from "@/views/Area";

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'Index',
            component: Index
        },
        {
            path: '/area',
            name: 'Area',
            component: Area
        },
        {
            path: '/about',
            name: 'About',
            component: About
        }
    ]
})