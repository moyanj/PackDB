import { createWebHistory, createRouter } from 'vue-router'

import HomeView from './views/Home.vue'
import SearchView from './views/Search.vue'
import ListView from './views/List.vue'
import AboutView from './views/About.vue'
import PackageView from './views/Package.vue'

const routes = [
    { path: '/', component: HomeView },
    { path: '/search', component: SearchView },
    { path: '/list', component: ListView },
    { path: '/about', component: AboutView },
    { path: '/package/:name', component: PackageView }
]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})