<template>
    <div class='tokens-result'>
        <h3>Tokens:</h3>
        <ul>
            <li v-for='(token, index) in result.data.tokens' :key='index' class='token-item'
                :title='formatLocation(token.location)'>
                <span>{{ token.text }} ({{ token.type }})</span>
            </li>
        </ul>
    </div>
</template>

<script>
export default {
    props: {
        result: Object
    },
    methods: {
        formatLocation(location) {
            return `File: ${location.file}, Line: ${location.line}, Column: ${location.column}`
        }
    }
}
</script>

<style>
.tokens-result {
    border: 1px solid #ddd;
    padding: 10px;
}

.token-item {
    cursor: help;
}
</style>
