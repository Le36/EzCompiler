<template>
    <div class="dropdown-container" @mouseover="openDropdown" @mouseleave="closeDropdown" @click="openDropdown"
         tabindex="0">
        <button class="dropdown-toggle">
            Select Code Example
            <span v-if="isOpen">&#9650;</span>
            <span v-else>&#9660;</span>
        </button>
        <transition name="fade" @before-enter="beforeEnter" @enter="enter" @leave="leave">
            <div class="dropdown-menu" v-if="isOpen">
                <a v-for="example in codeExamples" :key="example.name" class="dropdown-item"
                   @click.prevent="selectExample(example.code)"
                   @mouseover="currentExplanation = example.explanation"
                   @mouseleave="currentExplanation = ''">
                    {{ example.name }}
                </a>
            </div>
        </transition>
        <div class="tooltip" v-if="currentExplanation" v-text="currentExplanation"></div>
    </div>
</template>

<script>
export default {
    name: 'CustomDropdown',
    data() {
        return {
            isOpen: false,
            currentExplanation: '',
            codeExamples: [
                {name: 'Example 1', code: 'console.log("Example 1");', explanation: 'Logs a message to the console.'},
                {name: 'Example 2', code: 'console.log("Example 2");', explanation: '1233123132'},
                {name: 'Example 3', code: 'console.log("Example 3");', explanation: 'yes'}
            ]
        }
    },
    methods: {
        openDropdown() {
            this.isOpen = !this.isOpen
        },
        closeDropdown() {
            this.isOpen = false
            this.currentExplanation = ''
        },
        selectExample(code) {
            this.$emit('codeSelected', code)
            this.closeDropdown()
        },
        beforeEnter(el) {
            el.style.opacity = 0
        },
        enter(el, done) {
            el.style.transition = 'opacity 0.5s ease'
            el.style.opacity = 1
            done()
        },
        leave(el, done) {
            el.style.opacity = 0
            el.addEventListener('transitionend', done)
        }
    }
}
</script>


<style scoped>
.dropdown-container {
    position: relative;
    display: inline-block;
}

.dropdown-toggle {
    background: none;
    color: #00bd7e;
    padding: 10px;
    border: #565656 1px solid;
    cursor: pointer;
    outline: none;
    border-radius: 5px;
}

.dropdown-toggle:focus {
    box-shadow: 0 0 0 2px rgba(0, 189, 126, 0.4);
}

.dropdown-menu {
    position: absolute;
    margin-top: 10px;
    background-color: rgba(58, 58, 58, 0.8);
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
    z-index: 100;
    border-radius: 5px;
}

.dropdown-item {
    color: var(--color-text);
    padding: 12px 16px;
    text-decoration: black;
    display: block;
}

.dropdown-item:hover {
    background-color: rgba(0, 189, 126, 0.8);
    border-radius: 5px;
}

.tooltip {
    position: absolute;
    top: 0;
    left: 100%;
    transform: translateX(10px);
    background-color: rgba(0, 189, 126, 0.68);
    border: 1px solid #ccc;
    color: white;
    padding: 8px;
    margin-top: 5px;
    width: auto;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    z-index: 1000;
}

.fade-enter-active, .fade-leave-active {
    transition: opacity 0.5s ease;
}

.fade-enter, .fade-leave-to {
    opacity: 0;
}

</style>
