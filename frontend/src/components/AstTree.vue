<template>
    <div ref='astContainer' class='ast-container'></div>
</template>

<script>
import {Network, DataSet} from 'vis-network/standalone'

export default {
    props: ['astData'],
    data() {
        return {
            network: null
        }
    },
    watch: {
        astData() {
            this.network.destroy()
            this.createASTVisualization()
        }
    },
    mounted() {
        this.createASTVisualization()
    },
    methods: {
        createASTVisualization() {
            const container = this.$refs.astContainer
            const data = this.transformASTToVisData(this.astData)
            const options = {
                layout: {
                    hierarchical: {
                        enabled: true,
                        direction: 'UD',
                        sortMethod: 'directed',
                        nodeSpacing: 110,
                        treeSpacing: 200,
                        levelSeparation: 100,
                        shakeTowards: 'roots'
                    }
                },
                nodes: {
                    shape: 'box',
                    color: {
                        background: '#212121',
                        border: '#00bd7e',
                        hover: {
                            background: 'rgba(0,189,126,0.65)',
                            border: '#00bd7e'
                        },
                        highlight: {
                            background: 'rgba(0,189,126,0.65)',
                            border: '#00ef9f'
                        }
                    },
                    font: {
                        color: '#00bd7e',
                        size: 18
                    }
                },
                edges: {
                    smooth: {
                        type: 'cubicBezier',
                        forceDirection: 'vertical',
                        roundness: 0.4
                    },
                    arrows: 'to',
                    color: 'gray',
                    font: {
                        color: 'white',
                        strokeColor: 'black',
                        size: 16
                    }
                },
                interaction: {
                    hover: true,
                    navigationButtons: true,
                    keyboard: true,
                    tooltipDelay: 100
                },
                physics: {
                    enabled: false
                },
                manipulation: {
                    enabled: false
                }
            }

            this.network = new Network(container, data, options)
        },
        transformASTToVisData(ast) {
            const nodes = []
            const edges = []

            const traverse = (node, parentId = null, relation = '') => {
                if (typeof node !== 'object' || node === null) return

                const nodeId = nodes.length + 1
                let label
                let locationInfo = `Line: ${node.location.line}, Column: ${node.location.column}`

                if ('value' in node) {
                    if (typeof node.value === 'object' && node.value !== null) {
                        label = `Var: ${node.name}`
                    } else {
                        label = `Literal: ${node.value}`
                    }
                } else if ('name' in node && 'arguments' in node) {
                    label = `Call: ${node.name}`
                } else if ('name' in node) {
                    label = `Identifier: ${node.name}`
                } else if ('op' in node && 'left' in node && 'right' in node) {
                    label = `BinaryOp: ${node.op}`
                } else if ('op' in node) {
                    label = `UnaryOp: ${node.op}`
                } else if ('condition' in node && 'then_branch' in node) {
                    label = 'If'
                } else if ('expressions' in node || 'result_expression' in node) {
                    label = '{ ... }'
                } else if ('condition' in node && 'body' in node) {
                    label = 'While'
                } else {
                    label = 'Unknown'
                }

                nodes.push({id: nodeId, label, title: locationInfo})

                if (parentId) {
                    edges.push({from: parentId, to: nodeId, label: relation, arrows: 'to'})
                }

                if (node.left) traverse(node.left, nodeId, 'left')
                if (node.right) traverse(node.right, nodeId, 'right')
                if (node.condition) traverse(node.condition, nodeId, 'condition')
                if (node.then_branch) traverse(node.then_branch, nodeId, 'then')
                if (node.else_branch) traverse(node.else_branch, nodeId, 'else')
                if (node.arguments) node.arguments.forEach((arg) => traverse(arg, nodeId, 'args'))
                if (node.operand) traverse(node.operand, nodeId, 'operand')
                if (node.expressions) node.expressions.forEach((expr) => traverse(expr, nodeId, 'expr'))
                if (node.result_expression) traverse(node.result_expression, nodeId, 'result')
                if (node.body) traverse(node.body, nodeId, 'body')
                if (node.value && typeof node.value === 'object') traverse(node.value, nodeId, 'initializer')
            }

            traverse(ast)

            return {
                nodes: new DataSet(nodes),
                edges: new DataSet(edges)
            }
        }
    }
}
</script>
<style>
.ast-container {
    width: 100%;
    height: 498px;
}

div.vis-button.vis-zoomIn {
    border: rgb(0, 189, 126) 1px solid !important;
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="rgba(0, 189, 126)" d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32V224H48c-17.7 0-32 14.3-32 32s14.3 32 32 32H192V432c0 17.7 14.3 32 32 32s32-14.3 32-32V288H400c17.7 0 32-14.3 32-32s-14.3-32-32-32H256V80z"/></svg>') !important;
    background-color: #212121 !important;
    background-position: center !important;
    background-size: contain !important;
}

div.vis-button.vis-zoomIn:hover {
    box-shadow: #00bd7e 0 0 10px !important;
}

div.vis-button.vis-zoomOut {
    border: rgb(0, 189, 126) 1px solid !important;
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="rgba(0, 189, 126)" d="M432 256c0 17.7-14.3 32-32 32L48 288c-17.7 0-32-14.3-32-32s14.3-32 32-32l352 0c17.7 0 32 14.3 32 32z"/></svg>') !important;
    background-color: #212121 !important;
    background-position: center !important;
    background-size: contain !important;
}

div.vis-button.vis-zoomOut:hover {
    box-shadow: #00bd7e 0 0 10px !important;
}

div.vis-button.vis-zoomExtends {
    border: rgb(0, 189, 126) 1px solid !important;
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="rgba(0, 189, 126)" d="M9.4 9.4C21.9-3.1 42.1-3.1 54.6 9.4L160 114.7V96c0-17.7 14.3-32 32-32s32 14.3 32 32v96c0 4.3-.9 8.5-2.4 12.2c-1.6 3.7-3.8 7.3-6.9 10.3l-.1 .1c-3.1 3-6.6 5.3-10.3 6.9c-3.8 1.6-7.9 2.4-12.2 2.4H96c-17.7 0-32-14.3-32-32s14.3-32 32-32h18.7L9.4 54.6C-3.1 42.1-3.1 21.9 9.4 9.4zM256 256a64 64 0 1 1 128 0 64 64 0 1 1 -128 0zM114.7 352H96c-17.7 0-32-14.3-32-32s14.3-32 32-32h96 0l.1 0c8.8 0 16.7 3.6 22.5 9.3l.1 .1c3 3.1 5.3 6.6 6.9 10.3c1.6 3.8 2.4 7.9 2.4 12.2v96c0 17.7-14.3 32-32 32s-32-14.3-32-32V397.3L54.6 502.6c-12.5 12.5-32.8 12.5-45.3 0s-12.5-32.8 0-45.3L114.7 352zM416 96c0-17.7 14.3-32 32-32s32 14.3 32 32v18.7L585.4 9.4c12.5-12.5 32.8-12.5 45.3 0s12.5 32.8 0 45.3L525.3 160H544c17.7 0 32 14.3 32 32s-14.3 32-32 32H448c-8.8 0-16.8-3.6-22.6-9.3l-.1-.1c-3-3.1-5.3-6.6-6.9-10.3s-2.4-7.8-2.4-12.2l0-.1v0V96zM525.3 352L630.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L480 397.3V416c0 17.7-14.3 32-32 32s-32-14.3-32-32V320v0c0 0 0-.1 0-.1c0-4.3 .9-8.4 2.4-12.2c1.6-3.8 3.9-7.3 6.9-10.4c5.8-5.8 13.7-9.3 22.5-9.4c0 0 .1 0 .1 0h0 96c17.7 0 32 14.3 32 32s-14.3 32-32 32H525.3z"/></svg>') !important;
    background-color: #212121 !important;
    background-position: center !important;
    background-size: contain !important;
}

div.vis-button.vis-zoomExtends:hover {
    box-shadow: #00bd7e 0 0 10px !important;
}

div.vis-button.vis-up {
    border: rgb(0, 189, 126) 1px solid !important;
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="rgba(0, 189, 126)" d="M214.6 41.4c-12.5-12.5-32.8-12.5-45.3 0l-160 160c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L160 141.2V448c0 17.7 14.3 32 32 32s32-14.3 32-32V141.2L329.4 246.6c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3l-160-160z"/></svg>') !important;
    background-color: #212121 !important;
    background-position: center !important;
    background-size: contain !important;
}

div.vis-button.vis-up:hover {
    box-shadow: #00bd7e 0 0 10px !important;
}

div.vis-button.vis-left {
    border: rgb(0, 189, 126) 1px solid !important;
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="rgba(0, 189, 126)" d="M9.4 233.4c-12.5 12.5-12.5 32.8 0 45.3l160 160c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3L109.2 288 416 288c17.7 0 32-14.3 32-32s-14.3-32-32-32l-306.7 0L214.6 118.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0l-160 160z"/></svg>') !important;
    background-color: #212121 !important;
    background-position: center !important;
    background-size: contain !important;
}

div.vis-button.vis-left:hover {
    box-shadow: #00bd7e 0 0 10px !important;
}

div.vis-button.vis-right {
    border: rgb(0, 189, 126) 1px solid !important;
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="rgba(0, 189, 126)" d="M438.6 278.6c12.5-12.5 12.5-32.8 0-45.3l-160-160c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3L338.8 224 32 224c-17.7 0-32 14.3-32 32s14.3 32 32 32l306.7 0L233.4 393.4c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l160-160z"/></svg>') !important;
    background-color: #212121 !important;
    background-position: center !important;
    background-size: contain !important;
}

div.vis-button.vis-right:hover {
    box-shadow: #00bd7e 0 0 10px !important;
}

div.vis-button.vis-down {
    border: rgb(0, 189, 126) 1px solid !important;
    background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2024 Fonticons, Inc.--><path fill="rgba(0, 189, 126)" d="M169.4 470.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 370.8 224 64c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 306.7L54.6 265.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z"/></svg>') !important;
    background-color: #212121 !important;
    background-position: center !important;
    background-size: contain !important;
}

div.vis-button.vis-down:hover {
    box-shadow: #00bd7e 0 0 10px !important;
}

div.vis-tooltip {
    background-color: #212121 !important;
    color: #00bd7e !important;
    border: 1px solid #00bd7e !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5) !important;
    padding: 5px !important;
}
</style>
