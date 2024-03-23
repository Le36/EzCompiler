<template>
    <div class="console-window">
        <div class="console-titlebar">
            <span class="title">Interpreter Output</span>
            <button class="close-btn" @click="clearConsole">
                <font-awesome-icon icon="times" />
            </button>
        </div>
        <div class="console-container">
            <div class="console-output" ref="consoleOutput">
                <div v-for="(line, index) in lines" :key="index" class="console-line">{{ line }}</div>
            </div>
        </div>
    </div>
</template>

<script>
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

export default {
    components: {FontAwesomeIcon},
    data() {
        return {
            lines: [],
            currentInput: ''
        }
    },
    methods: {
        printLine(line) {
            this.lines.push(line)
            this.$nextTick(() => {
                const outputContainer = this.$refs.consoleOutput
                outputContainer.scrollTop = outputContainer.scrollHeight
            })
        },
        clearConsole() {
            this.lines = []
        }
    }
}
</script>

<style scoped>
.console-window {
    border: #00bd7e 1px solid;
    width: 300px;
    font-family: 'Consolas', 'Courier New', monospace;
    box-shadow: 0 0 12px 5px rgba(0, 0, 0, 0.2);
}

@media (min-width: 1024px) {
    .console-window {
        width: 400px;
    }
}

.console-titlebar {
    background-color: var(--vt-c-black-soft);
    color: #00bd7e;
    padding: 5px 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    user-select: none;
    cursor: default;
}

.console-titlebar .title {
    font-weight: bold;
}

.console-titlebar .close-btn {
    color: #00bd7e;
    background: none;
    border: none;
    cursor: pointer;
}

.console-container {
    background-color: #000000;
    color: #00bd7e;
    border-top: #00bd7e 1px solid;
    padding: 10px;
    height: 400px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow: hidden;
}

.console-output {
    flex-grow: 1;
    scrollbar-color: #00bd7e transparent;
    scrollbar-width: thin;
    overflow: auto;
}

.console-line {
    white-space: pre-wrap;
    word-break: break-word;
    overflow-wrap: break-word;
}

.close-btn {
    font-size: 20px;
    cursor: pointer;
}
</style>
