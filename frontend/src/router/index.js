// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        component: () => import('@/layouts/default/DefaultLayout.vue'),
        children: [
            {
                path: '/',
                redirect: { name: 'home' },
            },
            {
                path: '/home',
                name: 'home',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/HomeView.vue'
                    ),
            },
            {
                path: '/login',
                name: 'login',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/LoginView.vue'
                    ),
            },
            {
                path: '/register',
                name: 'register',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/LoginView.vue'
                    ),
            },

            {
                path: '/dashboard',
                name: 'dashboard',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/HomeView.vue'
                    ),
            },
        ],
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
})

export default router
