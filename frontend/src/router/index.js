import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'result',
        component: () => import('../views/ResultView.vue')
    },
    {
        path: '/tokenizer',
        name: 'tokenizer',
        component: () => import('../views/TokenizerView.vue')
    },
    {
        path: '/parser',
        name: 'parser',
        component: () => import('../views/ParserView.vue')
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

export default router
