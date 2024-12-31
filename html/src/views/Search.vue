<script setup lang="ts">
import { ElRow, ElCol, ElInput, ElButton, ElScrollbar, ElPagination } from 'element-plus';
import { ref, watch, Ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { Engine } from '../search';
import { PackageInfo } from '../data';
import pack from '../components/pack.vue';

const searchQuery = ref('');
const box_length = ref(10);
const data_length = ref(0);
const router = useRouter();
const route = useRoute();
const data: Ref<Array<null | {
    name: string;
    data: PackageInfo;
}>> = ref([]);
var db: Engine = new Engine(searchQuery.value);


watch(
    () => route.fullPath,
    async () => {
        if (route.query.q) {
            box_length.value = 24;
            searchQuery.value = route.query.q as string;
            db = new Engine(searchQuery.value);
            await db.load()
            data_length.value = db.getLength();
            if (data_length.value > 0) {
                data.value = await db.getCurrentPageData();
            }
        }
    },
    { immediate: true }
);
function handleSearch() {
    // 搜索按钮点击后的处理逻辑
    if (searchQuery.value.trim() !== '') {
        router.push("/search?q=" + searchQuery.value)
    } else {
        alert('请输入搜索内容');
    }
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

</script>

<template>
    <el-row justify="center" align="middle" style="margin-top: 40px;" v-if="!$route.query.q">
        <h1>PackDB</h1>
    </el-row>
    <el-row class="search-box" justify="center" align="middle">
        <el-col :span="box_length">
            <el-input v-model="searchQuery" placeholder="请输入搜索内容" class="search-input">
                <template #append>
                    <el-button @click="handleSearch">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                            class="bi bi-search" viewBox="0 0 16 16">
                            <path
                                d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z" />
                        </svg> 搜索
                    </el-button>
                </template>
            </el-input>
        </el-col>
    </el-row>

    <el-scrollbar class="packs" v-if="data_length > 0">
        <pack v-for="i in data" :i="i" />

    </el-scrollbar>
    <div v-else>没有找到相关内容</div>
    <div class="page" v-if="data_length > 0">
        <el-pagination layout="prev, pager, next" :total="data_length" :page-size="15" @prev-click="prev"
            @next-click="next" @current-change="currentChange" />
    </div>
</template>

<style scoped>
.search-box {
    padding: 20px;
}

.search-input {
    width: 100%;
    /* 圆角设计 */
    padding-right: 10px;
    /* 给按钮留空间 */
    height: 10%;
}

.el-input .el-input__inner {
    height: 40px;
    /* 调整输入框高度 */
    font-size: 14px;
    /* 字体大小 */
    padding-left: 15px;
    /* 输入框左侧内边距 */
    border: 1px solid #dcdfe6;
    /* 边框颜色 */
}

.el-button {
    border-radius: 30px;
    /* 圆角按钮 */
    padding: 0 20px;
    /* 按钮左右内边距 */
    height: 100%;
    /* 按钮高度与输入框一致 */
    font-size: 14px;
    /* 字体大小 */
}

.el-row {
    margin-bottom: 0;
    /* 去除底部间距 */
}

@media (max-width: 768px) {
    .search-box {
        padding: 15px;
    }

    .el-col {
        padding: 0;
    }
}

.page {
    display: flex;
    justify-content: center;
    height: 10%;
}

.packs {
    margin-top: 20px;
    height: 70%;
    padding: 10px;
}
</style>
