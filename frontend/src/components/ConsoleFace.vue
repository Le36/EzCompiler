<template>
    <div class='console-container'>
        <div class='console-output' ref='consoleOutput'>
            <div v-for='(line, index) in lines' :key='index' class='console-line'>{{ line }}</div>
        </div>
        <input
            type='text'
            class='console-input'
            v-model='currentInput'
            @keyup.enter='handleInput'
            placeholder='Enter command...'
        />
    </div>
</template>

<script>
export default {
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
        handleInput() {
            this.$emit('inputReceived', this.currentInput)
            this.currentInput = ''
        }
    },
    mounted() {
        this.printLine('Welcome to the console!')
    }
}
</script>

<style scoped>
.console-container {
    background-color: #333319;
    color: #e5ffff;
    border: #e5ffff 1px solid;
    font-family: 'Consolas', 'Courier New', monospace;
    padding: 10px;
    height: 300px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    scrollbar-color: #e5ffff transparent;
    scrollbar-width: thin;
}

.console-output {
    flex-grow: 1;
    overflow-y: auto;
}

.console-input {
    background-color: #333319;
    border: #e5ffff 1px solid;
    color: #e5ffff;
    padding: 5px;
    font-family: inherit;
}

.console-input:focus {
    outline: none;
}

.console-line {
    white-space: pre;
}
</style>
