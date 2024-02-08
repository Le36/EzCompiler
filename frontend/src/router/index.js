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
        path: '/ast',
        name: 'ast',
        component: () => import('../views/AstView.vue')
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

export default router
