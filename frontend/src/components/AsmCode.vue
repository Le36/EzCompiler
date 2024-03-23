<template>
    <div class="asm-view">
        <div class="asm-scrollable">
            <div class="asm-code-container" v-html="highlightedCode"></div>
        </div>
    </div>
    <div class="button-container">
        <pre v-if="!fileGenerated" class="error-message">Error: No executable file was generated.</pre>
        <button v-if="fileGenerated" @click="downloadExecutable" class="btn btn-primary">Download</button>
        <span v-if="fileGenerated">
            Download executable, invoked using the
            <a href="https://sourceware.org/binutils/docs-2.41/as.html" target="_blank" rel="noopener noreferrer"
                >GNU Assembler</a
            >
            for assembly-to-machine code translation.
        </span>
    </div>
</template>

<script>
export default {
    props: {
        result: String,
        fileGenerated: Boolean
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
    overflow: auto;
    font-family: 'Consolas', monospace;
    font-size: 14px;
    white-space: pre-wrap;
    word-wrap: break-word;
}

.asm-scrollable {
    max-height: 450px;
    width: 350px;
    padding: 35px 10px 35px 10px;
    overflow-y: auto;
}

.btn {
    display: flex;
    justify-content: space-evenly;
    margin: 5px;
    padding: 10px 15px;
    font-size: 16px;
    cursor: pointer;
    text-align: center;
    text-decoration: none;
    outline: none;
    color: #fff;
    background-color: #00bd7e;
    border: none;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}

.btn:hover {
    background-color: #006141;
    transition: background-color 0.3s ease;
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

.error-message {
    display: flex;
    color: #ff3860;
    justify-content: space-around;
}

.button-container {
    display: flex;
    font-size: 10px;
    align-items: center;
    max-height: 50px;
}

@media (min-width: 1024px) {
    .button-container {
        display: flex;
        font-size: 14px;
    }

    .asm-scrollable {
        width: 500px;
    }
}
</style>
