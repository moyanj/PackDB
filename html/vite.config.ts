import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
    plugins: [vue()],
    build: {
        chunkSizeWarningLimit: 20480,
        rollupOptions: {
            output: {
                manualChunks: {
                    'framework': ['vue', 'element-plus', 'vue-router', 'marked'],
                },
                entryFileNames: 'assets/main-[hash].js',
                chunkFileNames: 'assets/js/[name]-[hash].js', // 指定分片文件的输出路径及命名规则
                assetFileNames(assetInfo) {
                    //文件名称
                    if (assetInfo.names[0].endsWith('.css')) {
                        return 'assets/css/[name]-[hash].css'
                    }
                    if (assetInfo.names[0].endsWith('.woff') || assetInfo.names[0].endsWith('.woff2')) {
                        return 'assets/fonts/[name]-[hash].[ext]'
                    }
                    //剩余资源文件
                    return 'assets/[name]-[hash].[ext]'
                }
            }
        }
    }
})
