<template>
    <div>
        <div id="editor" style="height: 300px; width: 300px"></div>
        <button @click="submitCode">Submit</button>
    </div>
</template>

<script>
import ace from 'ace-builds/src-noconflict/ace'
import 'ace-builds/src-noconflict/theme-monokai'
import 'ace-builds/src-noconflict/mode-javascript'
import CompilerService from '@/services/CompilerService'

export default {
    name: 'CodeEditor',
    data() {
        return {
            editor: null
        }
    },
    mounted() {
        this.editor = ace.edit('editor')
        this.editor.setTheme('ace/theme/monokai')
        this.editor.session.setMode('ace/mode/javascript')
    },
    methods: {
        async submitCode() {
            const code = this.editor.getValue()
            try {
                await CompilerService.submitCode(code)
            } catch (error) {
                console.error(error)
            }
        }
    }
}
</script>

<style></style>
