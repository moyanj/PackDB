<script setup lang="ts">
import { ElMenu, ElMenuItem, ElButton } from "element-plus";
import { useRouter } from 'vue-router';
import { ref, watch } from "vue";

// 定义 active 引用的类型
const active = ref<string>("");

// 使用 useRouter 钩子
const router = useRouter();

// 监听路由变化以更新 active 引用
watch(
  () => router.currentRoute.value.path,
  (newPath) => {
    active.value = "/" + newPath.split("/")[1];
  },
  { immediate: true } // 立即执行一次以设置初始值
);

</script>

<template>
    <el-menu mode="horizontal" :ellipsis="false" :route="true" :default-active="active">
        <el-menu-item>
            <h2>PackDB</h2>
        </el-menu-item>

        <el-menu-item index="/" @click="router.push('/')" route="/">
            主页
        </el-menu-item>
        <el-menu-item index="/list" @click="router.push('/list')" route="/list">
            概览
        </el-menu-item>
        <el-menu-item index="/search" @click="router.push('/search')" route="/search">
            搜索
        </el-menu-item>
        <el-menu-item index="/about" @click="router.push('/about')" route="/about">
            关于
        </el-menu-item>
        <div class="tools">
            <el-button><i class="bi bi-box-seam-fill"></i>&nbsp;提交项目</el-button>
        </div>
    </el-menu>
    <div class="content">
        <RouterView />
    </div>
</template>

<style scoped>
.el-menu--horizontal>.el-menu-item:nth-child(1) {
    margin-right: auto;
}

.tools {
    display: flex;

    flex-direction: row;
    /*设置主轴方向是水平方向*/

    align-items: center;
    /*设置侧轴上，子元素的排列方式为居中对齐*/
    height: var(--el-menu-horizontal-height);
}

.content {
    position: relative;
    height: calc(100vh - var(--el-menu-horizontal-height) );
    overflow: hidden;
}
</style>
