<template>
    <pre class="code-result">
    {{ result }}
  </pre
    >
</template>

<script>
export default {
    props: {
        result: Object
    }
}
</script>

<style>
.code-result {
    border: 1px solid #ddd;
    padding: 10px;
}
</style>
