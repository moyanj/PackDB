import { createWebHistory, createRouter } from 'vue-router';
import Home from './views/Home.vue';
import Search from './views/Search.vue';
import List from './views/List.vue';
import About from './views/About.vue';
import Package from './views/Package.vue';

const routes = [
    { path: '/', component: Home },
    { path: '/search', component: Search },
    { path: '/list', component: List },
    { path: '/about', component: About },
    { path: '/package/:name', component: Package }
];

export const router = createRouter({
    history: createWebHistory(),
    routes,
});