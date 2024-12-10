<script setup lang="ts">
import { ElButton } from 'element-plus';
</script>

<template>
    <div class="title">
        <h1>PackDB</h1>
        <p>发现那些让代码飞起来的Python包</p>
    </div>
    <div class="menu">
        <el-button size="large" round type="primary" @click="$router.push('/list')">去浏览</el-button>
        <el-button size="large" round type="primary" @click="$router.push('/search')">去搜索</el-button>
    </div>
</template>

<style scoped>
.title {
    position: absolute;
    top: calc(100% / 3);
    height: calc(95% - (100% / 3));
    margin-left: 35px;
    width: 35%;
}

.menu {
    height: 95%;
    width: 65%;
    position: absolute;
    left: 35%;

    display: flex;
    justify-content: center;
    /* 水平居中 */
    align-items: center;
    /* 垂直居中 */
}

.menu .el-button {
    margin-left: 25px;
}
</style>
