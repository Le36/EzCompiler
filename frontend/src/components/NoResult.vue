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
    color: grey;
    font-style: italic;
    width: 300px;
}
</style>
