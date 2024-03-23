<template>
    <div class="info-box">
        <h3>{{ title }}</h3>
        <div class="info-body" v-html="infoText"></div>
    </div>
</template>

<script>
import {computed} from 'vue'
import {useRoute} from 'vue-router'
import {marked} from 'marked'

export default {
    setup() {
        const route = useRoute()

        const title = computed(() => {
            const titles = {
                interpreter: 'Interpreter',
                tokenizer: 'Tokenizer',
                ast: 'Abstract Syntax Tree',
                ir: 'Intermediate Representation',
                asm: 'Assembly Code'
            }
            return titles[route.name] || 'Welcome'
        })

        const infoText = computed(() => {
            let markdownContent
            switch (route.name) {
                case 'interpreter':
                    markdownContent =
                        'An **interpreter** directly runs source code without the preliminary step of converting it into machine code, distinguishing it significantly from compilers. This immediacy allows for the execution of programs without the overhead associated with compilation processes.\n' +
                        '\n' +
                        '#### The Role of Abstract Syntax Trees (AST)\n' +
                        '\n' +
                        'At the heart of our interpreter lies the use of an **Abstract Syntax Tree (AST)**, a structural representation of the code that abstracts away the syntactic details. This tree enables a straightforward and efficient traversal and evaluation process. While some interpreters, aiming for efficiency, first convert the AST into a simpler form like bytecode, our approach evaluates the AST directly. This method offers a balance between performance and simplicity, making the development and learning process more intuitive and immediate.\n' +
                        '\n' +
                        '#### The Process of Interpretation\n' +
                        '\n' +
                        'The interpreter operates by recursively walking through the AST, evaluating each node based on its type. This could include:\n' +
                        '- Evaluating expressions and arithmetic operations to produce values.\n' +
                        '- Executing conditional statements and loops based on logical evaluations.\n' +
                        '- Invoking functions with evaluated arguments for dynamic execution.\n' +
                        '\n' +
                        'This recursive evaluation strategy is central to interpreting programming languages, as it allows for the dynamic execution of complex constructs represented within the AST.\n' +
                        '\n' +
                        '#### Advantages of Direct AST Interpretation\n' +
                        '\n' +
                        'Opting for an AST-based interpreter in our project brings several key benefits:\n' +
                        '- **Immediate Feedback**: Direct execution of source code facilitates a rapid development cycle, crucial for learning environments and iterative development processes.\n' +
                        '- **Simplicity and Clarity**: By working directly with the AST, we maintain a high level of code clarity and simplicity, making it easier to understand and extend the interpreter.\n' +
                        '- **Educational Value**: The directness of this approach aids in demystifying the execution process of programming languages, offering valuable insights into the fundamentals of language processing.'
                    break
                case 'tokenizer':
                    markdownContent =
                        '**Tokenizing** is the first step in the process of interpreting or compiling source code, where the text of the code is divided into a series of **tokens**. Tokens are the smallest units that have semantic meaning in the program, such as keywords, identifiers, operators, and literals.\n' +
                        '\n' +
                        '#### How Tokenizing Works\n' +
                        '\n' +
                        "The tokenizer scans the source code text linearly, character by character, grouping these characters into tokens based on the language's syntax rules. This process transforms the raw text into a structured format that is easier for the compiler or interpreter to understand.\n" +
                        '\n' +
                        'Consider the code snippet:\n' +
                        '\n' +
                        '```\n' +
                        'if a <= bee then print_int(123)\n' +
                        '```\n' +
                        '\n' +
                        'During tokenization, this snippet is transformed into a sequence of tokens:\n' +
                        '\n' +
                        '```\n' +
                        "['if', 'a', '<=', 'bee', 'then', 'print_int', '(', '123', ')']\n" +
                        '```\n' +
                        '\n' +
                        'Each token represents a meaningful element of the code: `if` is a keyword, `a` and `bee` are identifiers, `<=` is an operator, and so on.\n' +
                        '\n' +
                        '#### The Importance of Tokenizing\n' +
                        '\n' +
                        'By breaking down the source code into tokens, we simplify the subsequent **parsing** stage. Parsing involves analyzing the sequence of tokens to determine the grammatical structure of the code. Without tokenization, the parser would have to deal with the raw text, significantly complicating the parsing logic.\n' +
                        '\n' +
                        'Furthermore, tokenizing:\n' +
                        '- **Enhances Error Detection**: Early identification of unrecognized tokens can help catch syntax errors.\n' +
                        '- **Optimizes Parsing**: With a clean, tokenized input, the parser can focus on the syntactic structure without getting bogged down by lexical analysis.\n' +
                        '- **Facilitates Syntax Highlighting**: Editors use tokenization to apply syntax highlighting, improving code readability.\n' +
                        '\n' +
                        '#### Beyond Simple Tokenizing\n' +
                        '\n' +
                        'While tokenizing primarily deals with identifying and classifying pieces of the code, it can also include:\n' +
                        '- Removing comments and whitespace, which are not relevant for parsing.\n' +
                        '- Classifying tokens further into types, literals, operators, etc., providing more context for the parsing stage.\n' +
                        '\n' +
                        'Tokenizing, therefore, is not just a preliminary step but a foundational one that impacts the efficiency and effectiveness of the entire compilation or interpretation process.'
                    break
                case 'ast':
                    markdownContent =
                        '**Parsing** converts a list of tokens into an **Abstract Syntax Tree (AST)**, organizing tokens into a hierarchical structure where operations are linked to their operands.\n' +
                        '\n' +
                        "For example, consider the expression `a + b * c`, tokenized as `['a', '+', 'b', '*', 'c']`. The corresponding AST is structured as follows:\n" +
                        '\n' +
                        '```\n' +
                        '    +\n' +
                        '   / \\\n' +
                        '  a   *\n' +
                        '     / \\\n' +
                        '    b   c\n' +
                        '```\n' +
                        '\n' +
                        'This tree illustrates the program executing the `+` operation with two parameters:\n' +
                        '- The variable `a`\n' +
                        '- The result of executing the `*` operation with `b` and `c` as parameters\n' +
                        '\n' +
                        'An AST for a function call like `f(x, g(x), y + 3)` is visualized as:\n' +
                        '\n' +
                        '```\n' +
                        '    f\n' +
                        '  / | \\\n' +
                        ' x  g  +\n' +
                        '    |  / \\\n' +
                        '    x y   3\n' +
                        '```\n' +
                        '\n' +
                        'This represents calling function `f` with parameters:\n' +
                        '- The variable `x`\n' +
                        '- The result of calling function `g` with `x`\n' +
                        '- The result of the `+` operation on `y` and the constant `3`\n' +
                        '\n' +
                        "Similarly, control flow expressions like `if x > 10 then print_int(x) else print_int(y)` are structured in ASTs to clarify the program's operations and their execution order:\n" +
                        '\n' +
                        '```\n' +
                        '     if\n' +
                        '   /  |  \\\n' +
                        '  >   |   else\n' +
                        ' / \\  |   /   \\\n' +
                        'x  10 print  print\n' +
                        '     |       |\n' +
                        '     x       y\n' +
                        '```\n' +
                        '\n' +
                        "ASTs elucidate the required operations and their sequence, streamlining the program's analysis, interpretation, and compilation."
                    break
                case 'ir':
                    markdownContent =
                        'The **Intermediate Representation (IR)** is a code formulation closer to machine code than an AST but structured as a list of simple instructions. Unlike the tree structure of an AST, IR is linear, making it a pivotal step towards generating machine code in the Assembly generator stage.\n' +
                        '\n' +
                        'Each compiler designs its own IR to fit the specific language it compiles. IR can vary in abstraction levels:\n' +
                        '\n' +
                        '- **High-level IR** is more abstract, focusing on simplifying analysis and transformation.\n' +
                        '- **Low-level IR** is closer to machine code, aiding in machine-specific optimizations and translation across different systems.\n' +
                        '#### Example of IR Instructions\n' +
                        'Consider the expression `f(a + 3)`; the corresponding IR might look like this:\n' +
                        '\n' +
                        '```\n' +
                        '# Load constant 3 into variable x1.\n' +
                        'LoadIntConst(3, x1)\n' +
                        '\n' +
                        '# Add variables a and x1, storing the result in x2.\n' +
                        'Call(+, [a, x1], x2)\n' +
                        '\n' +
                        '# Call function f with argument x2, storing the output in x3.\n' +
                        'Call(f, [x2], x3)\n' +
                        '```\n' +
                        '\n' +
                        "Our IR assumes an infinite set of abstract variables (`a`, `x1`, …) and uses a unified `Call` command for invoking operators and functions. It's the Assembly generator's job to map these abstract variables to concrete memory locations or registers and to differentiate between basic operations and function calls.\n" +
                        '#### Significance of IR\n' +
                        'While not strictly mandatory, employing an IR divides code generation into simpler parts. It facilitates many analyses and optimizations that are challenging to perform directly on machine code. By providing a level of abstraction, IR enables more efficient code generation and transformation processes, laying the groundwork for the final translation into machine code.'
                    break
                case 'asm':
                    markdownContent =
                        'The **Assembly Generator** is the final step in our compiler, transforming Intermediate Representation (IR) code into **Assembly language**. This form of code is one step closer to machine code, which is executable by computers.\n' +
                        '\n' +
                        '#### Introduction to Assembly Code\n' +
                        '\n' +
                        "Assembly language varies by the **processor's instruction set**. Our focus is on the **x86-64 family of processors**, predominant in Windows and Linux PCs. Processors have **registers**, small, fast memory locations for temporary data storage. For instance, x86-64 general-purpose registers include `%rax`, `%rbx`, `%rcx`, etc.\n" +
                        '\n' +
                        'Assembly instructions, such as `addq %rbx, %rax`, perform operations directly on these registers. However, computers require the binary format of these instructions, known as **machine code**. An **assembler** translates Assembly code into machine code.\n' +
                        '\n' +
                        '#### Main Memory and Machine Instructions\n' +
                        '\n' +
                        'Beyond registers, data is stored in **main memory**. It’s accessed via memory addresses, with pointers often pointing to these addresses. The `movq` instruction is pivotal for moving data between registers and memory. For example, `movq %rax, %rbx` copies data from `%rax` to `%rbx`, whereas `movq (%rax), %rbx` moves data from a memory location pointed to by `%rax` to `%rbx`.\n' +
                        '\n' +
                        '#### Compiling and Downloading Executables\n' +
                        '\n' +
                        'Our platform not only displays the generated Assembly code but also offers a **download button** for the compiled and linked executable. This file can be run on Linux machines using `./executable.out`.\n' +
                        '\n' +
                        'The backend assembler creates `program.s` from your Assembly code and utilizes the **GNU assembler** to produce object files like `stdlib.o` and `program.o`. These files contain machine code, initialization data, and labels necessary for the executable.\n' +
                        '\n' +
                        '**Linking** these object files is the last step to producing the final executable. Our system calls the GNU linker (`ld`), creating a minimal executable without external dependencies, such as the C standard library.\n'
                    break
                default:
                    markdownContent = 'Select a feature from the menu to get started.'
            }
            return marked(markdownContent)
        })

        return {title, infoText}
    }
}
</script>

<style>
.info-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 350px;
    border: #00bd7e 1px solid;
    border-top: 0;
    padding: 15px;
    color: var(--color-text);
    overflow-y: auto;
    max-height: 500px;
}

.info-box h3 {
    color: #00bd7e;
    margin: -10px 0 10px 0;
    font-weight: 500;
    padding-right: 20px;
    padding-left: 20px;
    border-right: var(--color-border) 2px solid;
    border-left: var(--color-border) 2px solid;
}

@media (min-width: 1024px) {
    .info-box {
        width: 1000px;
        max-height: 280px;
    }
}

.info-body h1,
.info-body h2,
.info-body h3,
.info-body h4,
.info-body h5,
.info-body h6 {
    color: #00bd7e;
    margin-top: 20px;
    margin-bottom: 20px;
}

.info-body h1 {
    font-size: 24px;
}

.info-body h2 {
    font-size: 20px;
}

.info-body p {
    margin-bottom: 15px;
}

.info-body strong {
    font-weight: bold;
}

.info-body ul,
.info-body ol {
    margin-left: 20px;
    margin-bottom: 10px;
    list-style-type: disc;
}

.info-body li {
    margin-bottom: 5px;
}

.info-body code {
    background-color: #333;
    padding: 2px 4px;
    border-radius: 4px;
    font-family: monospace;
    word-break: break-word;
    text-wrap: wrap;
}

.info-body pre {
    background-color: #333;
    padding: 10px;
    border-radius: 4px;
    margin-bottom: 15px;
}
</style>
