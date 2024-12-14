<script setup lang="ts">
import { useRoute } from 'vue-router';
import { ref, Ref, nextTick } from 'vue';
import { db, PackageInfo, ReleasesInfo } from '../data';
import { ElCard, ElRow, ElCol, ElScrollbar, ElButton, ElDivider, ElDialog, ElCollapse, ElCollapseItem } from 'element-plus';
import badger from '../components/badger.vue';
import { marked } from 'marked';

// 获取当前路由参数
const route = useRoute();
const name = route.params.name as string;

// 定义数据状态，明确类型
const packageInfo: Ref<PackageInfo | null> = ref(null);
const doc_html: Ref<string> = ref("<p>正在加载</p>");
const show_rel_data: Ref<boolean> = ref(false);
const data: Ref<ReleasesInfo | null> = ref(null);
const show_rel_name = ref('')
const rels = ref()
const show_ins = ref(false)

// 异步获取数据
async function fetchData() {
    try {
        // 调用数据库方法获取数据
        const result = await db.get(name);
        packageInfo.value = result;
        doc_html.value = await marked(result.doc, {
            silent: true,
            gfm: true
        });
        rels.value = packageInfo?.value.releases.reverse();
    } catch (error) {
        console.error('获取数据失败:', error);
    }
}

function show_rel(name: string) {
    show_rel_name.value = name;
    show_rel_data.value = true;
    data.value = packageInfo.value?.releases.filter(item => item.name === name)[0] as ReleasesInfo;
}


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

function renderSize(filesize: number) {
    var unitArr = new Array("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB");
    var index = 0;
    var srcsize = filesize
    index = Math.floor(Math.log(srcsize) / Math.log(1024));
    var size = srcsize / Math.pow(1024, index);
    var rsize = size.toFixed(2); //保留的小数位数
    return rsize + unitArr[index];
}

function to(url: string) {
    window.location.href = url
}

function copyCommand(type: string) {

    // 获取 div 元素的文本内容
    var copyEle = document.getElementById(type);
    if (!copyEle) {
        alert("复制失败!");
        return
    }
    var copyText = copyEle.textContent as string;

    // 使用 Clipboard API 复制内容
    navigator.clipboard.writeText(copyText).then(function () {
        alert("文本已复制: " + copyText);
    }).catch(function (err) {
        alert("复制失败: " + err);
    });

}

// 加载数据
nextTick(fetchData);
</script>


<template>
    <el-scrollbar v-if="packageInfo">
        <el-row>
            <el-card class="big-card summary">
                <el-row>
                    <el-col :span="17" :offset="1">
                        <h3>{{ name }}</h3>
                        <p>{{ packageInfo?.desc }}</p>
                    </el-col>

                    <el-col :span="6" class="center">
                        <el-button type="primary" @click="show_ins = true;">安装 {{ name }}</el-button>
                    </el-col>
                </el-row>

            </el-card>
        </el-row>
        <el-row :gutter="0">
            <el-col :span="5">
                <el-card class="big-card info">
                    <h5>标签</h5>
                    <badger v-for="k in packageInfo?.keywords" @click="to(`/search?q=${k}`)">
                        {{ k }}
                    </badger>
                    <el-divider />

                    <p>作者：{{ packageInfo?.author }}</p>
                    <p>作者邮箱：<a :href="'mailto:' + packageInfo?.author_email">{{ packageInfo?.author_email }}</a></p>
                    <el-divider />

                    <p>最新版本：{{ packageInfo?.latest }}</p>
                    <p>版本数量：{{ packageInfo?.releases.length }}</p>
                    <p>Python需求：{{ packageInfo?.requires_python }}</p>
                    <p>依赖({{ packageInfo?.requires.length }}个)：{{ packageInfo?.requires.join(", ") }}</p>
                    <el-divider />

                    <h5>项目链接：</h5>

                    <p v-if="packageInfo.project_urls" v-for="k in Object.keys(packageInfo?.project_urls)"><a
                            :href="packageInfo?.project_urls[k]">{{ k
                            }}</a></p>
                    <p v-else>无</p>
                    <el-divider />

                    <h5>版本数据（最新20个）</h5>
                    <div class="release-list">
                        <p v-for="rel in packageInfo?.releases" @click="show_rel(rel.name)" class="rel-link"
                            :key="rel.name">
                            {{ rel.name }}
                        </p>
                    </div>
                    <el-divider />


                    <h5>分类器</h5>
                    <p v-for="k in packageInfo?.classifiers">{{ k }}</p>
                </el-card>
            </el-col>
            <el-col :span="19"><el-card class="big-card markdown-body" v-html="doc_html"></el-card></el-col>
        </el-row>
    </el-scrollbar>

    <el-dialog v-model="show_rel_data as unknown as boolean" :title="name + ' ' + show_rel_name">
        <p>版本名：{{ show_rel_name }}</p>
        <p>发布时间：{{ ts2date(data?.files[0].upload_time as number) }}</p>
        <el-scrollbar style="height: 300px;">
            <el-collapse>
                <el-collapse-item v-for="n in data?.files" :title="n.file_name">
                    <p>大小：{{ renderSize(n.size) }}</p>
                    <p>MD5校验值: {{ n.digests.md5 }}</p>
                    <p>SHA256校验值: {{ n.digests.sha256 }}</p>
                    <p>blake2b_256校验值: {{ n.digests.blake2b_256 }}</p>
                </el-collapse-item>
            </el-collapse>
        </el-scrollbar>
    </el-dialog>

    <el-dialog v-model="show_ins" title="安装">
        <el-row class="cmds">
            <el-col class="type" :span="3">pip</el-col>
            <el-col class="cmd" id="pip" :span="18">pip install {{ name }}</el-col>
            <el-col class="copy" :span="3" @click="copyCommand('pip')"><i class="bi bi-clipboard"></i>复制</el-col>
        </el-row>
        <el-row class="cmds">
            <el-col class="type" :span="3">poetry</el-col>
            <el-col class="cmd" id="portry" :span="18">portry install {{ name }}</el-col>
            <el-col class="copy" :span="3" @click="copyCommand('poetry')"><i class="bi bi-clipboard"></i>复制</el-col>
        </el-row>
        <el-row class="cmds">
            <el-col class="type" :span="3">pipenv</el-col>
            <el-col class="cmd" id="pipenv" :span="18">pipenv install {{ name }}</el-col>
            <el-col class="copy" :span="3" @click="copyCommand('pipenv')"><i class="bi bi-clipboard"></i>复制</el-col>
        </el-row>
    </el-dialog>
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

.markdown-body {
    padding: 20px;
}

.info {
    font-size: small;
}

.release-list {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    /* 设置间距 */
}

.rel-link {
    box-sizing: border-box;
    /* 包括间距的宽度 */
    text-decoration: underline;
}

.cmds {
    margin-top: 10px;
    background-color: #25282b;
    /* 深色背景 */
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.type,
.cmd,
.copy {
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ecf0f1;
    /* 文字颜色，确保在暗色背景上可见 */
}

.type {
    font-weight: bold;
    color: #1abc9c;
    /* 'pip' 的绿色 */
}

.cmd {
    text-align: right;
    word-wrap: break-word;
}

.copy {
    text-align: center;
}
</style>
