<template>
    <div></div>
</template>

<script>
import {inject, onMounted, watch} from 'vue'
import SymTab from '@/utils/SymTab.js'

export default {
    props: {
        astData: Object
    },
    setup(props, {emit}) {
        const consoleComponent = inject('consoleComponent')
        const symTab = new SymTab()

        const printInt = (values) => {
            values.forEach(value => consoleComponent.value.printLine(value.toString()))
        }

        const printBool = (values) => {
            values.forEach(value => consoleComponent.value.printLine(value ? 'true' : 'false'))
        }

        const readInt = async () => {
            const input = await getInputFromConsole() // TODO: Implement this function
            return parseInt(input, 10)
        }

        const interpret = (node) => {
            if (!node) return null

            if ('value' in node) {
                return typeof node.value === 'object' ? interpret(node.value) : node.value
            }

            if ('op' in node && 'left' in node && 'right' in node) {
                const leftVal = interpret(node.left)
                const rightVal = interpret(node.right)
                switch (node.op) {
                    case '+':
                        return leftVal + rightVal
                    case '-':
                        return leftVal - rightVal
                    default:
                        emit('error', `Unsupported binary operation: ${node.op}`)
                        return null
                }
            }

            if ('name' in node && 'value' in node) {
                const value = interpret(node.value)
                symTab.declareVar(node.name, value)
                return value
            }

            if ('name' in node && !('arguments' in node)) {
                return symTab.lookupVar(node.name)
            }

            if ('condition' in node && 'then_branch' in node) {
                return interpret(node.condition) ? interpret(node.then_branch) : interpret(node.else_branch)
            }

            if ('name' in node && 'arguments' in node) {
                switch (node.name) {
                    case 'print_int':
                        printInt(node.arguments.map(arg => interpret(arg)))
                        return null
                    case 'print_bool':
                        printBool(node.arguments.map(arg => interpret(arg)))
                        return null
                    case 'read_int':
                        return readInt()
                    default:
                        // Handle user-defined or unimplemented functions
                        emit('error', `Unimplemented function: ${node.name}`)
                        return null
                }
            }

            emit('error', `Unknown node type: ${node.type}`)
            return null
        }

        const startInterpretation = () => {
            const result = interpret(props.astData)
            if (consoleComponent.value) {
                consoleComponent.value.printLine(`Result: ${result}`)
            }
        }


        watch(() => props.astData, () => {
            startInterpretation()
        })

        onMounted(() => {
            startInterpretation()

        })

        return {consoleComponent}
    }
}
</script>