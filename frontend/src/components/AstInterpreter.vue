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
    setup(props) {
        const consoleComponent = inject('consoleComponent')
        const symTab = new SymTab()

        const printInt = (values) => {
            values.forEach((value) => consoleComponent.value.printLine(value.toString()))
        }

        const printBool = (values) => {
            values.forEach((value) => consoleComponent.value.printLine(value ? 'true' : 'false'))
        }

        const interpret = (node) => {
            if (!node) return null

            if ('op' in node && node.op === '=') {
                if ('name' in node.left) {
                    const varName = node.left.name
                    const newValue = interpret(node.right)
                    symTab.updateVar(varName, newValue)
                    return newValue
                } else {
                    console.error('Invalid assignment target.')
                    return null
                }
            } else if ('value' in node) {
                if (typeof node.value === 'object' && node.value !== null) {
                    symTab.declareVar(node.name, interpret(node.value))
                    return interpret(node.value)
                } else {
                    return node.value
                }
            } else if ('name' in node && 'arguments' in node) {
                const argsValues = node.arguments.map((arg) => interpret(arg))
                if (node.name === 'print_int') {
                    printInt(argsValues)
                } else if (node.name === 'print_bool') {
                    printBool(argsValues)
                }
                return null
            } else if ('name' in node) {
                return symTab.lookupVar(node.name)
            } else if ('op' in node && 'left' in node && 'right' in node) {
                const leftVal = interpret(node.left)
                const rightVal = interpret(node.right)
                return evalBinaryOp(node.op, leftVal, rightVal)
            } else if ('op' in node) {
                const operand = interpret(node.operand)
                return evalUnaryOp(node.op, operand)
            } else if ('condition' in node && 'then_branch' in node) {
                return interpret(node.condition) ? interpret(node.then_branch) : interpret(node.else_branch)
            } else if ('expressions' in node || 'result_expression' in node) {
                symTab.pushScope()
                let lastVal = null
                node.expressions.forEach((expr) => {
                    lastVal = interpret(expr)
                })
                if (node.result_expression) {
                    lastVal = interpret(node.result_expression)
                }
                symTab.popScope()
                return lastVal
            } else if ('condition' in node && 'body' in node) {
                while (interpret(node.condition)) {
                    interpret(node.body)
                }
                return null
            } else {
                console.error('Unknown node structure')
                return null
            }
        }

        const evalBinaryOp = (op, leftVal, rightVal) => {
            switch (op) {
                case '+':
                    return leftVal + rightVal
                case '-':
                    return leftVal - rightVal
                case '*':
                    return leftVal * rightVal
                case '/':
                    return leftVal / rightVal
                case '%':
                    return leftVal % rightVal
                case '==':
                    return leftVal === rightVal
                case '!=':
                    return leftVal !== rightVal
                case '<':
                    return leftVal < rightVal
                case '>':
                    return leftVal > rightVal
                case '<=':
                    return leftVal <= rightVal
                case '>=':
                    return leftVal >= rightVal
                default:
                    console.error(`Unsupported binary operator: ${op}`)
                    return null
            }
        }

        const evalUnaryOp = (op, operand) => {
            switch (op) {
                case '!':
                    return !operand
                case '-':
                    return -operand
                default:
                    console.error(`Unsupported unary operator: ${op}`)
                    return null
            }
        }

        const startInterpretation = () => {
            const result = interpret(props.astData)
            if (consoleComponent.value && result !== null) {
                consoleComponent.value.printLine(`Result: ${result}`)
            }
        }

        watch(
            () => props.astData,
            () => {
                startInterpretation()
            }
        )

        onMounted(() => {
            startInterpretation()
        })

        return {consoleComponent}
    }
}
</script>
