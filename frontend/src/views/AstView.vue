<template>
    <div>
        <NoResult v-if="!codeResult" />
        <AstTree v-else :astData="codeResult.data.ast" />
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
        const codeResult = computed(() => compilerStore.codeResult)

        return {codeResult}
    }
}
</script>
