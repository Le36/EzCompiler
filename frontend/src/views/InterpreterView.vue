<template>
    <div>
        <AstInterpreter
            v-if="astResult.compilation && Object.keys(astResult.compilation).length > 0"
            :astData="astResult.compilation.data.ast"
            ref="interpreter"
        />
        <ConsoleFace ref="consoleComponent" />
    </div>
</template>

<script>
import {ref, computed, provide, watch, onMounted} from 'vue'
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
        const astResult = computed(() => compilerStore)
        const consoleComponent = ref(null)
        provide('consoleComponent', consoleComponent)

        watch(
            () => astResult.value.error,
            (newError) => {
                if (newError && consoleComponent.value) {
                    consoleComponent.value.printLine(newError)
                }
            }
        )

        onMounted(() => {
            if (astResult.value.error && consoleComponent.value) {
                consoleComponent.value.printLine(astResult.value.error)
            }
        })

        return {consoleComponent, astResult}
    }
}
</script>
