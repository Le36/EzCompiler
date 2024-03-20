<template>
    <div v-if="isVisible" class="modal-overlay">
        <div class="modal-header">
            <span
                class="modal-title"
                @mousedown="startDrag"
                @mousemove="onDrag"
                @mouseup="stopDrag"
                @mouseleave="stopDrag"
                @touchstart="startDrag"
                @touchmove="onDrag"
                @touchend="stopDrag"
                @touchcancel="stopDrag"
                >Language Specification</span
            >
            <font-awesome-icon class="close-icon" icon="times" @click="$emit('close')" />
        </div>
        <div class="modal-body" v-html="parsedMarkdown"></div>
    </div>
</template>

<script>
import {marked} from 'marked'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import {library} from '@fortawesome/fontawesome-svg-core'
import {faTimes} from '@fortawesome/free-solid-svg-icons'

library.add(faTimes)

export default {
    components: {
        FontAwesomeIcon
    },
    props: ['markdownContent', 'isVisible'],
    data() {
        return {
            isDragging: false,
            startX: 0,
            startY: 0
        }
    },
    computed: {
        parsedMarkdown() {
            return marked(`
Language spec
=============

This language is a minimalist, dynamically typed programming language designed for educational purposes and simple scripting tasks. The syntax and semantics are intentionally straightforward to facilitate learning about language design, parsing, and evaluation mechanisms. The language supports basic arithmetic, control flow constructs (if-then-else, while loops), and function calls, making it suitable for implementing algorithms and simple applications.

The design focuses on clear and concise constructs, aiming to make the language both easy to implement and use. While simplicity is a key goal, the language is powerful enough to demonstrate fundamental programming concepts such as iteration and conditional branching.

Example
-------

The following example demonstrates a program written in this language. It implements the Collatz conjecture algorithm, which is a sequence of operations on an initial number to eventually reach the number 1. The program prints each step of the sequence:

\`\`\`javascript
{
\tvar n = 50;
\tprint_int(n);
\twhile n > 1 do {
\t    if n % 2 == 0 then {
\t        n = n / 2;
\t    } else {
\t        n = 3 * n + 1;
\t    }
\t    print_int(n);
\t}
}
\`\`\`

Syntax
------

The syntax defines the formal structure of valid programs. A program is composed of expressions, which are the fundamental building blocks that can produce a value. The syntax is recursively defined to allow complex expressions built from simpler ones. Here are the core elements:

- **Integer literal:** Represents a 64-bit signed integer ranging from -2^64 to 2^63 - 1.
- **Boolean literal:** Either \`true\` or \`false\`.
- **Identifier:** A sequence of letters, digits, and underscores, not starting with a digit.
- **Unary operator:** Either \`-E\` for negation or \`not E\` for boolean negation.
- **Binary operator:** Combines two expressions (\`E1 op E2\`) using operators for arithmetic (\`+\`, \`-\`, \`*\`, \`/\`, \`%\`), comparison (\`==\`, \`!=\`, \`<\`, \`<=\`, \`>\`, \`>=\`), logical (\`and\`, \`or\`), or assignment (\`=\`).
  - The assignment operator (\`=\`) is right-associative, meaning it evaluates from right to left.
  - All other binary operators are left-associative, evaluating from left to right.
  - Operators have defined precedences, specified below, to determine the order of evaluation in complex expressions.
- **Parentheses** (\`(E)\`) alter the natural precedence to enforce a specific evaluation order.
- **Block:** A sequence of expressions enclosed in \`{}\`. Blocks can be empty, and the trailing semicolon is optional.
- **Untyped variable declaration:** Introduces a new variable within a block using \`var ID = E\`.
- **Conditional expressions:** Include \`if E1 then E2\` and \`if E1 then E2 else E3\` for branching logic.
- **While-loop:** Repeatedly executes a block as long as a condition is true (\`while E1 do E2\`).
- **Built-in function call:** Executes a function with given arguments (\`ID(E1, E2, ..., En)\`).


Variable declarations (\`var ...\`) are allowed only directly inside blocks (\`{ ... }\`).

Precedences:

1.  \`=\`
2.  \`or\`
3.  \`and\`,
4.  \`==\`, \`!=\`
5.  \`<\`, \`<=\`, \`>\`, \`>=\`
6.  \`+\`, \`-\`
7.  \`*\`, \`/\`, \`%\`
8.  Unary \`-\` and \`not\`
9.  All other constructs: literals, identifiers, \`if\`, \`while\`, \`var\`, blocks, parentheses, function calls.

All non-operator expressions such as \`if\`, \`while\` and function calls must be (syntactically) allowed to be part of other expressions, so e.g. \`1 + if true then 2 else 3\` are allowed.

The **program** consists of a single expression, called the **top-level expression**. If multiple expressions are given, they are treated like a block without \`{\` and \`}\`.

Whitespace and comments (both single-line \`#\` or \`//\` and multi-line \`/* ... */\`) are ignored except as separators between tokens.

Semantics
---------

The semantics of our language outline how programs are interpreted or executed, defining the runtime behavior of various constructs. This section serves as a guideline for implementing an interpreter or compiler that accurately reflects the designed language behavior, ensuring consistency across different implementations.

**Values:**

In our language, a value can be one of the following types:

- **64-bit signed integer:** Represents numeric values within the range of -2^64 to 2^63 - 1, suitable for most arithmetic operations.
- **Boolean:** Either \`true\` or \`false\`, used in logical expressions and conditional statements.
- **Built-in function:** A predefined function provided by the language runtime, such as \`print_int\` for outputting integers.
- **Unit:** A special value indicating the absence of a meaningful value, analogous to \`void\` in C or Java, used primarily in the context of statements or functions that do not return a value.

**Context:**

The execution context is crucial for variable scoping and resolution. It is composed of:

- **Locals:** A mapping from identifiers to values representing the current scope.
- **Parent context (optional):** A reference to an enclosing scope's context, enabling nested scopes and the lookup of identifiers not found in the current scope.

**Evaluation Rules:**

The evaluation of expressions is detailed below, ensuring a clear understanding of how each construct behaves:

- **Literals:** Return their inherent value (integer or boolean).
- **Identifiers:** Look up the current or nearest enclosing scope for the value. If not found, evaluation fails.
- **Unary operators (\`-\`, \`not\`):** Apply the operation to the value of the expression. If the type does not match the expected (e.g., \`not\` used on an integer), the operation fails.
- **Binary operators:** Include arithmetic, logical, and comparison operations. The order of evaluation respects operator precedence, and type mismatches result in failure.
- **Assignment (\`=\`):** Updates the value of an identifier in the current or nearest modifiable enclosing scope. If the identifier does not exist, evaluation fails.
- **Blocks:** Evaluate each expression in sequence, in a new scope if necessary. The value of the last expression (if any) is returned, or \`unit\` if the block ends with a statement.
- **Conditional expressions:** Evaluate the condition and execute the corresponding block based on its boolean value. If the condition is not a boolean, evaluation fails.
- **Loops (\`while\`):** Continuously evaluate the block as long as the condition evaluates to true. Loops return \`unit\`.
- **Built-in function calls:** Evaluate each argument expression in order, then call the function with these values. If the function identifier does not correspond to a built-in or defined function, evaluation fails.

**Error Handling:**

The language design ensures robustness through explicit error handling rules for undefined identifiers, type mismatches, and other potential runtime errors. This approach aids developers in debugging and ensures predictable program behavior.

**Built-in Functions:**

These functions provide basic I/O functionalities and other utilities essential for a minimalistic programming language. Their implementation is part of the runtime environment:

- \`print_int\`: Outputs an integer followed by a newline.
- \`print_bool\`: Outputs a boolean (\`true\` or \`false\`) followed by a newline.
- \`read_int\`: This function reads an integer from standard input. Should the input fail to represent a valid integer, the resulting behavior is left intentionally undefined to provide flexibility in handling errors. It's important to note that this functionality is not supported within the frontend interpreter but is exclusively available in the assembled or compiled program.

**Program Output:**

The output of a program includes any side effects from built-in function calls (e.g., printed text) and the value of the top-level expression, if it produces an integer or boolean value. This design supports a wide range of programs, from those that primarily perform computations and return a result to those that interact with the user through input and output.

`)
        }
    },
    methods: {
        startDrag(event) {
            this.isDragging = true
            if (event.touches) {
                event.preventDefault()
                this.startX = event.touches[0].clientX - this.$el.offsetLeft
                this.startY = event.touches[0].clientY - this.$el.offsetTop
            } else {
                this.startX = event.clientX - this.$el.offsetLeft
                this.startY = event.clientY - this.$el.offsetTop
            }
        },
        onDrag(event) {
            if (!this.isDragging) return
            let clientX, clientY
            if (event.touches) {
                clientX = event.touches[0].clientX
                clientY = event.touches[0].clientY
            } else {
                clientX = event.clientX
                clientY = event.clientY
            }
            this.$el.style.left = `${clientX - this.startX}px`
            this.$el.style.top = `${clientY - this.startY}px`
        },
        stopDrag() {
            this.isDragging = false
        }
    }
}
</script>

<style>
.modal-overlay {
    position: fixed;
    top: 15%;
    left: 15%;
    background: var(--color-background);
    border: 1px solid #00bd7e;
    box-shadow: 12px 12px 12px rgba(0, 0, 0, 0.2);
    z-index: 1050;
    display: flex;
    flex-direction: column;
    max-width: 550px;
    max-height: 500px;
}

.modal-header {
    background: var(--vt-c-black-soft);
    cursor: grab;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: #00bd7e;
}

.modal-title {
    font-weight: bold;
    padding: 5px 0 5px 10px;
    width: 100%;
}

.close-icon {
    cursor: pointer;
    font-size: 30px;
    padding: 5px 10px 5px 0;
}

.modal-body {
    overflow-y: auto;
    padding: 20px;
    height: 400px;
}

.modal-body h1,
.modal-body h2,
.modal-body h3,
.modal-body h4,
.modal-body h5,
.modal-body h6 {
    color: #00bd7e;
    margin-top: 20px;
    margin-bottom: 20px;
}

.modal-body h1 {
    font-size: 24px;
}

.modal-body h2 {
    font-size: 20px;
}

.modal-body p {
    margin-bottom: 15px;
}

.modal-body strong {
    font-weight: bold;
}

.modal-body ul,
.modal-body ol {
    margin-left: 20px;
    margin-bottom: 10px;
}

.modal-body li {
    margin-bottom: 5px;
}

.modal-body code {
    background-color: #333;
    padding: 2px 4px;
    border-radius: 4px;
    font-family: monospace;
}

.modal-body pre {
    background-color: #333;
    padding: 10px;
    border-radius: 4px;
    overflow-x: auto;
}
</style>
