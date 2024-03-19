<template>
    <div>
        <LanguageSpecModal :isVisible="showLangSpec" @close="showLangSpec = false" />
        <div id="editor"></div>
        <div class="compile-btn-container">
            <button class="submit-btn" @click="submitCode">Compile</button>
            <span
                >Initiate source code compilation or
                <a href="#" @click.prevent="showLanguageSpecModal">review the language spec</a> for syntax and semantics
                guidance.</span
            >
        </div>
    </div>
</template>

<script>
import ace from 'ace-builds/src-noconflict/ace'
import 'ace-builds/src-noconflict/theme-monokai'
import 'ace-builds/src-noconflict/mode-javascript'
import CompilerService from '@/services/CompilerService'
import LanguageSpecModal from '@/components/LanguageSpecModal.vue'

export default {
    name: 'CodeEditor',
    components: {
        LanguageSpecModal
    },
    data() {
        return {
            editor: null,
            showLangSpec: false
        }
    },
    mounted() {
        this.editor = ace.edit('editor')
        this.editor.setTheme('ace/theme/clouds_midnight')
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
        },
        setEditorCode(code) {
            if (this.editor) {
                this.editor.setValue(code, 1)
            }
        },
        showLanguageSpecModal() {
            this.showLangSpec = true
        }
    }
}
</script>

<style>
#editor {
    height: 451px;
    width: 100%;
    border-bottom: #00bd7e 1px solid;
}

.submit-btn {
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

.submit-btn:hover {
    background-color: #006141;
    transition: background-color 0.3s ease;
}

.compile-btn-container {
    display: flex;
    font-size: 14px;
}
</style>
