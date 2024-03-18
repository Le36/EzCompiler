<template>
    <div class="asm-code-container">
        <pre>{{ result }}</pre>
    </div>
</template>

<script>
export default {
    props: {
        result: String
    }
}
</script>

<style scoped>
.asm-code-container pre {
    background-color: #f5f5f5;
    color: #333;
    padding: 16px;
    overflow: auto;
    font-family: 'Courier New', Courier, monospace;
    white-space: pre-wrap;
    word-wrap: break-word;
    border-radius: 8px;
}
</style>
