<script setup lang="ts">
import { defineProps } from 'vue';

const props = defineProps({
    color: {
        type: String,
        default: "var(--el-fill-color)"
    },
    text: {
        type:String,
        default: "var(--el-text-color-primary)"
    }
});
</script>

<template>
    <span class="badger" :style="{ backgroundColor: props.color, color:props.text }">
        <slot></slot>
    </span>
</template>

<style scoped>
.badger {
    padding: 2px 4px;
    text-align: center;
    border-radius: 4px;
    font-size: 10px;
    margin-left: 2px;
    margin-right: 2px;
}
</style>