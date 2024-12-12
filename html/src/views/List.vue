<script setup lang="ts">
import { db } from '../data';
import { ref } from 'vue';
import { ElCard, ElScrollbar, ElRow, ElCol, ElButton, ElPagination } from 'element-plus';
import badger from '../components/badger.vue';

const data = ref()
function ts2date(ts: number) {
    let date = new Date(ts * 1000);

    const formattedDate = date.getFullYear() + '-' +
        ('0' + (date.getMonth() + 1)).slice(-2) + '-' +
        ('0' + date.getDate()).slice(-2) + ' ' +
        ('0' + date.getHours()).slice(-2) + ':' +
        ('0' + date.getMinutes()).slice(-2) + ':' +
        ('0' + date.getSeconds()).slice(-2);
    return formattedDate
}

function to(url: string) {
    window.open(url);
}

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
        <el-card v-for="i in data" @click="$router.push(`/package/${i.name}`)">
            <el-row>
                <!-- 包名 -->
                <el-col :span="3">
                    <p>{{ i["name"] }}</p>
                </el-col>

                <el-col :span="19">
                    <!-- 包介绍 -->
                    <el-row class="desc">
                        <span>{{ i.data.desc }}</span>
                    </el-row>
                    <!-- 标签 -->
                    <el-row>
                        <badger>数据更新时间：{{ ts2date(i.data.add_time) }}</badger>
                        <badger>最新版本：{{ i.data.latest ? i.data.latest : "无" }}</badger>
                        <badger>版本数量：{{ i.data.latest ? i.data.releases.length : "0" }}</badger>
                        <badger v-if='i.data.desc.includes("内置库")'>内置库</badger>
                    </el-row>
                </el-col>
                <el-col :span="1" class="tools">
                    <el-button round @click="$router.push('/')">详情</el-button>
                    <el-button round @click="to(i.data.url)">Pypi</el-button>
                </el-col>
            </el-row>
        </el-card>
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

.tools {
    display: flex;
    justify-content: center;
    /* 水平居中 */
    align-items: center;
    /* 垂直居中 */
}

span {
    font-size: 15px;
}

p {
    font-size: 18px;
}

.desc {
    margin-bottom: var(--el-card-padding)
}

.page {
    display: flex;
    justify-content: center;
    height: 10%;
}
</style>
