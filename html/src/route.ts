import { createWebHistory, createRouter } from 'vue-router'

const routes = [
    { path: '/', component: () => import('./views/Home.vue') },
    { path: '/search', component: () => import('./views/Search.vue') },
    { path: '/list', component: () => import('./views/List.vue') },
    { path: '/about', component: () => import('./views/About.vue') },
    { path: '/package/:name', component: () => import('./views/Package.vue') }
]

export const router = createRouter({
    history: createWebHistory(),
    routes,
})