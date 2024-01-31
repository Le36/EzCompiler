<template>
    <div>
        <NoResult v-if="!codeResult" />
        <CodeResult v-else :result="codeResult" />
    </div>
</template>

<script>
import {useCompilerStore} from '@/stores/compilerStore'
import {computed} from 'vue'
import NoResult from '@/components/NoResult.vue'
import CodeResult from '@/components/CodeResult.vue'

export default {
    components: {
        NoResult,
        CodeResult
    },
    setup() {
        const compilerStore = useCompilerStore()
        const codeResult = computed(() => compilerStore.codeResult)

        return {codeResult}
    }
}
</script>
