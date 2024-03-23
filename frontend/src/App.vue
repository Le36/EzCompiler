<script setup>
import {RouterView} from 'vue-router'
import HeaderRouter from './components/HeaderRouter.vue'
import CodeEditor from '@/components/CodeEditor.vue'
import InfoBox from '@/components/InfoBox.vue'
</script>

<script>
export default {
    methods: {
        setEditorCode(code) {
            this.$refs.codeEditor.setEditorCode(code)
        }
    }
}
</script>

<template>
    <HeaderRouter msg="EzCompiler" @codeSelected="setEditorCode" />
    <div class="bordered">
        <div class="wrapper">
            <div class="left-panel">
                <CodeEditor ref="codeEditor" />
            </div>
            <div class="right-panel">
                <RouterView />
            </div>
        </div>
        <InfoBox />
    </div>
</template>

<style scoped>
.left-panel,
.right-panel {
    border: #00bd7e 1px solid;
    width: 350px;
    height: 500px;
}

.right-panel {
    display: flex;
    justify-content: center;
    align-items: center;
    border-top: 0;
}

.bordered {
    box-shadow: 0 0 12px 5px rgba(0, 0, 0, 0.2);
}

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

    .left-panel,
    .right-panel {
        width: 500px;
        height: 501px;
    }

    .right-panel {
        border-left: 0;
        border-top: #00bd7e 1px solid;
    }
}
</style>
