<template>
    <div>
        <NoResult v-if="!codeResult" />
        <Tokenizer v-else :result="codeResult" />
    </div>
</template>

<script>
import {useCompilerStore} from '@/stores/compilerStore'
import {computed} from 'vue'
import NoResult from '@/components/NoResult.vue'
import Tokenizer from '@/components/Tokenizer.vue'

export default {
    components: {
        Tokenizer,
        NoResult,
    },
    setup() {
        const compilerStore = useCompilerStore()
        const codeResult = computed(() => compilerStore.codeResult)

        return {codeResult}
    }
}
</script>
