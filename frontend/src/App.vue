<script setup>
import {RouterView} from 'vue-router'
import HeaderRouter from './components/HeaderRouter.vue'
import CodeEditor from '@/components/CodeEditor.vue'
</script>

<template>
    <HeaderRouter msg="Custom Compiler" />
    <div class="wrapper">
        <div class="left-panel">
            <CodeEditor />
        </div>
        <div class="right-panel">
            <RouterView />
        </div>
    </div>
</template>

<style scoped>
@media (min-width: 1024px) {
    .wrapper {
        display: flex;
        flex-direction: row;
    }

    nav {
        text-align: left;
        margin-left: -1rem;
        font-size: 1rem;

        padding: 1rem 0;
        margin-top: 1rem;
    }
}
</style>
