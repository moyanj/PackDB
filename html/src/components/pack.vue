<script lang="ts" setup>
import { ElRow, ElCol, ElCard, ElButton } from 'element-plus';
import badger from './badger.vue';
import { PackageInfo } from '../data';

const props = defineProps<{
    i: { name: string, data: PackageInfo } | null
}>()

const i = props.i as { name: string, data: PackageInfo };
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
</script>

<template>
    <el-card @click="$router.push(`/package/${i.name}`)" class="pack">
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
</template>

<style lang="css" scoped>
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

.pack {
    margin-bottom: 20px;
}
</style>