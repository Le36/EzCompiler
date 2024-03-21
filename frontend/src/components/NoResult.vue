<template>
    <div class="no-result">
        {{ errorMessage || 'No result has been acquired yet.' }}
    </div>
</template>

<script>
export default {
    props: {
        errorMessage: String
    }
}
</script>

<style>
.no-result {
    color: var(--color-text);
    font-style: italic;
    width: 300px;
    text-align: center;
}
</style>
