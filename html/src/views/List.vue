<script setup lang="ts">
import { db } from '../data'
import { ref, nextTick } from 'vue';
import { ElScrollbar, ElPagination } from 'element-plus';
import pack from '../components/pack.vue';

const data = ref({});
function prev() {
    data.value = {};
    db.prevPage()
    db.getCurrentPageData().then(v => {
        nextTick(() => { data.value = v; })
    })

}
function next() {
    data.value = {};
    db.nextPage()
    db.getCurrentPageData().then(v => {
        nextTick(() => { data.value = v; })
    })

}

function currentChange(n: number) {
    data.value = {};
    db.goToPage(n);
    db.getCurrentPageData().then(v => {
        nextTick(() => { data.value = v; })
    })

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
