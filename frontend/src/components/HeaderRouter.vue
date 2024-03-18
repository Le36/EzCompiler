<script setup>
import {RouterLink} from 'vue-router'
import CodeExamplesSelector from '@/components/CodeExamples.vue'

defineProps({
    msg: {
        type: String,
        required: true
    }
})
</script>

<template>
    <div class="greetings">
        <h1 class="green">{{ msg }}</h1>
        <h3>Try custom compiler here</h3>
        <CodeExamplesSelector @codeSelected="$emit('codeSelected', $event)" />
        <nav>
            <RouterLink to="/">Interpreter</RouterLink>
            <RouterLink to="/tokenizer">Tokenizer</RouterLink>
            <RouterLink to="/ast">AST Tree</RouterLink>
            <RouterLink to="/ir">IR</RouterLink>
        </nav>
    </div>
</template>

<style scoped>
nav a {
    display: inline-block;
    padding: 0 1rem;
    border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
    border: 0;
}

h1 {
    font-weight: 500;
    font-size: 2.6rem;
    position: relative;
    top: -10px;
}

h3 {
    font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
    text-align: center;
}

@media (min-width: 1024px) {
    .greetings h1,
    .greetings h3 {
        text-align: left;
    }

    nav {
        text-align: left;
        margin-left: -1rem;
        font-size: 1rem;

        padding: 1rem 0;
        margin-top: 1rem;
    }
}
</style>
