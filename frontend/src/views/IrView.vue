<template>
    <div>
        <NoResult v-if="compilerOutput.error || !compilerOutput.compilation" :errorMessage="compilerOutput.error" />
        <IntermediateRepresentation v-else :result="compilerOutput.compilation.data.ir" />
    </div>
</template>

<script>
import {useCompilerStore} from '@/stores/compilerStore'
import {computed} from 'vue'
import NoResult from '@/components/NoResult.vue'
import IntermediateRepresentation from '@/components/IntermediateRepresentation.vue'

export default {
    components: {
        IntermediateRepresentation,
        NoResult
    },
    setup() {
        const compilerStore = useCompilerStore()
        const compilerOutput = computed(() => compilerStore)

        return {compilerOutput}
    }
}
</script>
