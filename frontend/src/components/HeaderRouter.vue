<script setup>
import {RouterLink} from 'vue-router'
import CodeExamplesSelector from '@/components/CodeExamples.vue'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

defineProps({
    msg: {
        type: String,
        required: true
    }
})
</script>

<template>
    <div class="greetings">
        <div class="title">
            <h1 class="green">
                <font-awesome-icon icon="fa-solid fa-microchip" />
                {{ msg }}
            </h1>
            <CodeExamplesSelector @codeSelected="$emit('codeSelected', $event)" />
        </div>
        <h3>
            Experience Hands-On Compilation with Our Custom EzLang on EzCompiler. View Project on
            <a href="https://github.com/Le36" target="_blank" rel="noopener noreferrer" class="github-link">
                GitHub
                <font-awesome-icon icon="fa-brands fa-github" />
            </a>
        </h3>

        <nav>
            <RouterLink to="/">Interpreter</RouterLink>
            <RouterLink to="/tokenizer">Tokenizer</RouterLink>
            <RouterLink to="/ast">AST (Abstract Syntax Tree)</RouterLink>
            <RouterLink to="/ir">IR (Intermediate Representation)</RouterLink>
            <RouterLink to="/asm">Assembly Code</RouterLink>
        </nav>
    </div>
</template>

<script>
import {library} from '@fortawesome/fontawesome-svg-core'
import {faMicrochip} from '@fortawesome/free-solid-svg-icons'
import {faGithub} from '@fortawesome/free-brands-svg-icons'

library.add(faGithub)
library.add(faMicrochip)
</script>

<style scoped>
.title {
    display: flex;
    flex-direction: column;
}

nav a {
    display: inline-block;
    padding: 0 1rem;
    border-left: 1px solid var(--color-border);
    border-right: 1px solid var(--color-border);
}

h1 {
    font-weight: 500;
    font-size: 3rem;
    position: relative;
}

h3 {
    font-size: 1.2rem;
    margin-bottom: 20px;
}

.greetings h1,
.greetings h3 {
    text-align: left;
}

nav {
    text-align: center;
    margin-top: 1rem;
    margin-bottom: 1rem;
    font-size: 1.2rem;
}

@media (min-width: 1024px) {
    nav {
        font-size: 1rem;
        border-right: 0;
    }

    nav a:first-of-type {
        border-left: 0;
    }

    nav a:last-of-type {
        border-right: 0;
    }

    .title {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
    }
}
</style>
