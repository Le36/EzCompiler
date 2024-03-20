<template>
    <div class="tokens-view">
        <div class="tokens-scrollable">
            <ul class="token-list">
                <li v-for="(token, index) in result.data.tokens" :key="index">
                    <Tooltip>
                        <template v-slot:default>
                            <div class="token-display">
                                <div class="token-info">
                                    <font-awesome-icon :icon="getIconForType(token.type)" class="token-icon" />
                                    <span class="token-type">{{ token.type.toLowerCase() }}</span>
                                </div>
                                <span class="token-value">{{ token.text }}</span>
                            </div>
                        </template>
                        <template v-slot:content>
                            Line: {{ token.location.line }}, Column: {{ token.location.column }}
                        </template>
                    </Tooltip>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
import Tooltip from './TooltipItem.vue'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'
import {faHashtag, faCheck, faPlus, faCode, faKeyboard, faIdBadge} from '@fortawesome/free-solid-svg-icons'

export default {
    components: {
        FontAwesomeIcon,
        Tooltip
    },
    props: {
        result: Object
    },
    methods: {
        getIconForType(type) {
            const icons = {
                INTEGER: faHashtag,
                BOOLEAN: faCheck,
                OPERATOR: faPlus,
                PUNCTUATION: faCode,
                KEYWORD: faKeyboard,
                IDENTIFIER: faIdBadge
            }
            return icons[type]
        }
    }
}
</script>

<style>
.tokens-view {
    padding: 5px;
}

.tokens-scrollable {
    max-height: 498px;
    width: 350px;
    padding: 35px 10px 35px 10px;
    overflow-y: auto;
}

li {
    list-style-type: none;
    padding: 0 5px 0 5px;
}

.token-list {
    padding-inline-start: 0;
    border: #00bd7e 1px solid;
}

.tokens-scrollable ul li:nth-child(even) {
    background-color: #212121;
}

.token-display {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.token-info {
    display: flex;
    align-items: center;
    gap: 10px;
}

.token-icon {
    color: hsla(160, 100%, 37%, 1);
    min-width: 35px;
}

.token-type {
    font-weight: v-bind(500);
    color: #3a3a3a;
    text-transform: capitalize;
    transition: color 0.3s ease;
}

.token-value {
    margin-left: auto;
    color: hsla(160, 100%, 37%, 1);
}

.tooltip:hover {
    .token-type {
        color: #00bd7e;
        transition: color 0.3s ease;
    }
}

@media (min-width: 1024px) {
    .tokens-scrollable {
        width: 500px;
    }
}
</style>
