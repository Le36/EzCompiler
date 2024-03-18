import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'interpreter',
        component: () => import('../views/InterpreterView.vue')
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
    },
    {
        path: '/ir',
        name: 'ir',
        component: () => import('../views/IrView.vue')
    },
    {
        path: '/asm',
        name: 'asm',
        component: () => import('../views/AsmView.vue')
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

export default router
