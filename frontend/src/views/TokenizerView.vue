<template>
    <div>
        <NoResult v-if="compilerOutput.error || !compilerOutput.compilation" :errorMessage="compilerOutput.error" />
        <Tokenizer v-else :result="compilerOutput.compilation" />
    </div>
</template>

<script>
import {useCompilerStore} from '@/stores/compilerStore'
import {computed} from 'vue'
import NoResult from '@/components/NoResult.vue'
import Tokenizer from '@/components/TokenizerList.vue'

export default {
    components: {
        Tokenizer,
        NoResult
    },
    setup() {
        const compilerStore = useCompilerStore()
        const compilerOutput = computed(() => compilerStore)

        return {compilerOutput}
    }
}
</script>
