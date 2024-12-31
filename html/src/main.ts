import { createApp } from 'vue';
import 'element-plus/dist/index.css';
import 'element-plus/theme-chalk/dark/css-vars.css';
// @ts-ignore
import 'github-markdown-css';
import './style.css';
import App from './App.vue';
import { router } from './route';
import { db } from './data';

async function main() {
    try {
        await db.load();

        // 创建 Vue 应用
        const app = createApp(App)
        app.use(router)
        app.mount('#app')
        
    } catch (error) {
        console.error('Failed to initialize application:', error);
    }
}

main();