<script setup lang="ts">
import { useRoute } from 'vue-router';
import { db } from '../data';
import { ElCard, ElRow, ElCol } from 'element-plus';

const route = useRoute();
const name = route.params.name as string;
const data = db.get(name);
console.log(data)

</script>

<template>
    <el-row>
        <el-card class="big-card summary">
            <el-row>
                <el-col :span="17" :offset="1">
                    <h3>{{ name }}</h3>
                    <p>{{ data?.desc }}</p>
                </el-col>
                <el-col :span="6" class="center">
                    <p>pip install {{ name }}</p>
                </el-col>
            </el-row>

        </el-card>
    </el-row>
    <el-row :gutter="0">
        <el-col :span="6"><el-card class="big-card"></el-card></el-col>
        <el-col :span="18"><el-card class="big-card"></el-card></el-col>
    </el-row>

</template>

<style scoped>
.big-card {
    margin-top: 15px;
    margin-left: 25px;
    margin-right: 10px;
    --el-card-padding: 15px;
}

.summary {
    width: 100%;
    height: 25vh;
}
.center {
    display: flex;
    justify-content: center;
    /* 水平居中 */
    align-items: center;
    /* 垂直居中 */
}
</style>
