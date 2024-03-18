<template>
    <div class="asm-view">
        <div class="asm-scrollable">
            <div class="asm-code-container" v-html="highlightedCode"></div>
        </div>
    </div>
    <button @click="downloadExecutable" class="btn btn-primary">Download Executable</button>
</template>

<script>
export default {
    props: {
        result: String
    },
    methods: {
        downloadExecutable() {
            const link = document.createElement('a')
            link.href = '/download/executable'
            link.setAttribute('download', '')
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
        },
        applySyntaxHighlighting(text) {
            text = text.replace(/(#.*$)/gm, "<span class='comment'>$1</span>")
            text = text.replace(
                /\b(movq|addq|subq|cmpq|jmp|jne|call|xor|setl|pushq|popq)\b/g,
                "<span class='instruction'>$1</span>"
            )
            text = text.replace(/(\.\w+)/g, "<span class='directive'>$1</span>")
            text = text.replace(/(%\w+\b)/g, "<span class='register'>$1</span>")

            return text
        }
    },
    computed: {
        highlightedCode() {
            let text = this.result

            const lines = text.split('\n')

            let previousWasDirectiveOrLabel = false
            const processedLines = lines.flatMap((line, index) => {
                let processedLine = line

                const isDirectiveOrLabel = line.startsWith('.') || line.match(/^\.\w+:/)
                if (isDirectiveOrLabel) {
                    previousWasDirectiveOrLabel = true
                    return [processedLine, '']
                } else {
                    if (previousWasDirectiveOrLabel) {
                        previousWasDirectiveOrLabel = false
                        return processedLine
                    } else {
                        return '  ' + processedLine
                    }
                }
            })
            text = processedLines.join('\n')

            text = this.applySyntaxHighlighting(text)

            return text
        }
    }
}
</script>

<style>
.asm-view {
    border-bottom: #00bd7e 1px solid;
}

.asm-code-container {
    color: #b5b5b5;
    padding: 16px;
    overflow: auto;
    font-family: 'Consolas', monospace;
    font-size: 14px;
    white-space: pre-wrap;
    word-wrap: break-word;
    border-radius: 8px;
    border: #00bd7e 1px solid;
}

.asm-scrollable {
    max-height: 430px;
    width: 500px;
    padding: 35px 10px 35px 10px;
    overflow-y: auto;
}

.btn {
    margin: 10px;
    display: flex;
    justify-content: space-evenly;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    text-align: center;
    text-decoration: none;
    outline: none;
    color: #fff;
    background-color: #00bd7e;
    border: none;
    border-radius: 5px;
}

.btn:hover {
    background-color: #006141;
}

.comment {
    color: hsla(160, 100%, 37%, 1);
}

.instruction {
    color: #c586c0;
}

.directive {
    color: #9cdcfe;
}

.register {
    color: #4ec9b0;
}
</style>
