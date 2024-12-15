<script setup lang="ts">
import { db } from '../data'
import { ref } from 'vue';
import { ElScrollbar, ElPagination } from 'element-plus';
import pack from '../components/pack.vue';

const data = ref()

async function prev() {
    db.prevPage()
    data.value = await db.getCurrentPageData()
}
async function next() {
    db.nextPage()
    data.value = await db.getCurrentPageData();
}

async function currentChange(n: number) {
    console.log(n)
    db.goToPage(n);
    data.value = await db.getCurrentPageData();
}
currentChange(1);
</script>

<template>
    <el-scrollbar class="packs">
        <pack v-for="i in data" :i="i" />
    </el-scrollbar>
    <div class="page">
        <el-pagination layout="prev, pager, next" :total="db.getLength()" :page-size="10" @prev-click="prev"
            @next-click="next" @current-change="currentChange" />
    </div>

</template>

<style scoped>
.el-card {
    margin-bottom: 20px;
}

.packs {
    margin-top: 20px;
    height: 80%;
    padding: 10px;
}

.page {
    display: flex;
    justify-content: center;
    height: 10%;
}
</style>
