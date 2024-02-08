<template>
    <div class="tooltip" @mouseover="show = true" @mouseleave="show = false">
        <slot></slot>
        <transition @before-enter="beforeEnter" @enter="enter" @leave="leave">
            <div v-if="show" class="tooltip-content">
                <slot name="content"></slot>
            </div>
        </transition>
    </div>
</template>

<script>
export default {
    data() {
        return {
            show: false
        }
    },
    methods: {
        beforeEnter(el) {
            el.style.opacity = 0
        },
        enter(el, done) {
            el.offsetHeight
            el.style.transition = 'opacity 0.3s ease'
            el.style.opacity = 1
            done()
        },
        leave(el, done) {
            el.style.opacity = 0
            el.style.transition = 'opacity 0.3s ease'
            done()
        }
    }
}
</script>

<style>
.tooltip {
    position: relative;
}

.tooltip-content {
    position: absolute;
    z-index: 10;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background-color: #2a2a2a;
    color: hsla(160, 100%, 37%, 1);
    text-align: center;
    padding: 5px;
    border-radius: 10px;
    width: 150px;
    user-select: none;
    white-space: nowrap;
    font-weight: v-bind(400);
    border: #00bd7e 1px solid;
}

.tooltip-content::after {
    content: ' ';
    position: absolute;
    top: 100%;
    left: 15%;
    margin-left: -10px;
    border-width: 5px;
    border-style: solid;
    border-color: #00bd7e transparent transparent transparent;
}
</style>
