<script setup lang="ts">
import { useRoute } from 'vue-router';
import { db } from '../data';

const route = useRoute();
const name = route.params.name as string;
const data = db.get(name);
console.log(data)

</script>

<template>
<h1>{{ $route.params.name }}</h1>

</template>

<style scoped>

</style>
