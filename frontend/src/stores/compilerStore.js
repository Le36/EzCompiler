import {defineStore} from 'pinia'

export const useCompilerStore = defineStore('compilerStore', {
    state: () => ({
        compilation: null,
        error: null
    }),
    actions: {
        setCompilationSuccess(newResult) {
            this.compilation = newResult
            this.error = null
        },
        setCompilationError(newError) {
            this.error = newError
            this.compilation = null
        }
    }
})
