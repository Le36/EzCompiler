<template>
    <div>
        <NoResult v-if="compilerOutput.error || !compilerOutput.compilation" :errorMessage="compilerOutput.error" />
        <AstTree v-else :astData="compilerOutput.compilation.data.ast" />
    </div>
</template>

<script>
import {useCompilerStore} from '@/stores/compilerStore'
import {computed} from 'vue'
import NoResult from '@/components/NoResult.vue'
import AstTree from '@/components/AstTree.vue'

export default {
    components: {
        AstTree,
        NoResult
    },
    setup() {
        const compilerStore = useCompilerStore()
        const compilerOutput = computed(() => compilerStore)

        return {compilerOutput}
    }
}
</script>
