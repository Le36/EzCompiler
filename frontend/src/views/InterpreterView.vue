<template>
    <div>
        <AstInterpreter
            v-if="astResult && Object.keys(astResult).length > 0"
            :astData="astResult.data.ast"
            ref="interpreter"
        />
        <ConsoleFace ref="consoleComponent" />
    </div>
</template>

<script>
import {ref, computed, provide} from 'vue'
import {useCompilerStore} from '@/stores/compilerStore'
import ConsoleFace from '@/components/ConsoleFace.vue'
import AstInterpreter from '@/components/AstInterpreter.vue'

export default {
    components: {
        ConsoleFace,
        AstInterpreter
    },
    data() {
        return {
            astData: null
        }
    },
    setup() {
        const compilerStore = useCompilerStore()
        const astResult = computed(() => compilerStore.codeResult)
        const consoleComponent = ref(null)
        provide('consoleComponent', consoleComponent)

        return {consoleComponent, astResult}
    }
}
</script>
