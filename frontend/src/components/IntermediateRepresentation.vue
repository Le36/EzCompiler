<template>
    <div class="ir-view">
        <div class="ir-scrollable">
            <ul class="ir-list">
                <li v-for="(instruction, index) in transformedIR" :key="index">
                    <TooltipItem>
                        <template v-slot:default>
                            <div class="ir-display" v-html="instruction.text"></div>
                        </template>
                        <template v-slot:content>
                            Line: {{ instruction.location.line }}, Column: {{ instruction.location.column }}
                        </template>
                    </TooltipItem>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
import TooltipItem from './TooltipItem.vue'

export default {
    components: {
        TooltipItem
    },
    props: {
        result: {
            type: Array,
            required: true
        }
    },
    computed: {
        transformedIR() {
            return this.transformIR(this.result)
        }
    },
    methods: {
        transformIR(irArray) {
            return [
                {
                    text: this.highlightSyntax('Label(start)'),
                    location: {line: '0', column: '0'}
                },
                ...irArray.map((instruction) => {
                    const {dest, value, source, args, fun, name, label, else_label, then_label, cond, location} =
                        instruction

                    let text = ''

                    if (label && !dest && !value && !source && !args && !fun && !name && !cond) {
                        text = `Jump(Label(${label.name}))`
                    } else if (value !== undefined) {
                        const valueType = typeof value === 'boolean' ? 'LoadBoolConst' : 'LoadIntConst'
                        text = `${valueType}(${value}, ${dest?.name})`
                    } else if (source !== undefined) {
                        text = `Copy(${source.name}, ${dest?.name})`
                    } else if (args !== undefined) {
                        const argNames = Array.isArray(args) ? args.map((arg) => arg.name) : [args.name]
                        text = `Call(${fun.name}, [${argNames.join(', ')}], ${dest?.name})`
                    } else if (name !== undefined) {
                        text = `Label(${name})`
                    } else if (cond !== undefined) {
                        text = `CondJump(${cond.name}, Label(${then_label?.name}), Label(${else_label?.name}))`
                    } else if (fun !== undefined && fun.name === 'print_int') {
                        const argList = Array.isArray(args) ? args.map((arg) => arg.name) : [args.name]
                        text = `Call(${fun.name}, [${argList}], ${dest?.name})`
                    }

                    return {
                        text: this.highlightSyntax(text),
                        location: location || {line: 'N/A', column: 'N/A'}
                    }
                }),
                {
                    text: this.highlightSyntax('Return()'),
                    location: {line: '0', column: '0'}
                }
            ]
        },
        highlightSyntax(text) {
            const keywords = ['Label', 'LoadIntConst', 'Copy', 'Call', 'CondJump', 'Jump', 'Return', 'LoadBoolConst']
            keywords.forEach((keyword) => {
                const regex = new RegExp(`\\b${keyword}\\b`, 'g')
                text = text.replace(regex, `<span class='keyword'>${keyword}</span>`)
            })
            text = text.replace(/\(/g, "<span class='parentheses'>(</span>")
            text = text.replace(/\)/g, "<span class='parentheses'>)</span>")
            text = text.replace(/\[/g, "<span class='brackets'>[</span>")
            text = text.replace(/]/g, "<span class='brackets'>]</span>")

            text = text.replace(/\btrue\b/g, "<span class='boolean'>true</span>")
            text = text.replace(/\bfalse\b/g, "<span class='boolean'>false</span>")

            text = text.replace(/\b\d+\b/g, "<span class='number'>$&</span>")

            text = text.replace(/\bx\d+\b/g, "<span class='address'>$&</span>")
            return text
        }
    }
}
</script>
<style>
.ir-view {
    padding: 5px;
}

.ir-scrollable {
    max-height: 498px;
    width: 350px;
    padding: 35px 10px 35px 10px;
    overflow-y: auto;
}

li {
    list-style-type: none;
    padding: 0 5px 0 5px;
}

.ir-list {
    padding-inline-start: 5px;
}

.ir-display {
    display: flex;
    font-family: 'Consolas', monospace;
    color: #7d7d7d;
    transition: color 0.3s ease;
}

.tooltip:hover {
    .ir-display {
        color: hsla(160, 100%, 37%, 1);
        background: #212121;
        transition: color 0.3s ease;
    }
}

.keyword {
    color: hsla(160, 100%, 37%, 1);
}

.parentheses {
    color: hsl(212, 100%, 69%);
}

.brackets {
    color: hsl(211, 61%, 31%);
}

.boolean {
    color: hsl(300, 76%, 72%);
}

.number {
    color: hsl(38, 100%, 50%);
}

.address {
    color: hsl(24, 54%, 60%);
}

@media (min-width: 1024px) {
    .ir-scrollable {
        width: 500px;
    }

    .ir-list {
        border: #00bd7e 1px solid;
    }
}
</style>
