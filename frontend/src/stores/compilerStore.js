import {defineStore} from 'pinia'

export const useCompilerStore = defineStore('compilerStore', {
    state: () => ({
        codeResult: ''
    }),
    actions: {
        setCodeResult(newResult) {
            this.codeResult = newResult
        }
    }
})
