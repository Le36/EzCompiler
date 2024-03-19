<template>
    <div>
        <NoResult v-if="compilerOutput.error || !compilerOutput.compilation" :errorMessage="compilerOutput.error" />
        <AsmCode
            v-else
            :result="compilerOutput.compilation.data.asm"
            :fileGenerated="compilerOutput.compilation.data.file_generated"
        />
    </div>
</template>

<script>
import {useCompilerStore} from '@/stores/compilerStore'
import {computed} from 'vue'
import NoResult from '@/components/NoResult.vue'
import AsmCode from '@/components/AsmCode.vue'

export default {
    components: {
        AsmCode,
        NoResult
    },
    setup() {
        const compilerStore = useCompilerStore()
        const compilerOutput = computed(() => compilerStore)

        return {compilerOutput}
    }
}
</script>
