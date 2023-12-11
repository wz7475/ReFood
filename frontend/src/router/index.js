// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        component: () => import('@/layouts/default/DefaultLayout.vue'),
        children: [
            {
                path: '',
                name: 'Home',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/HomeView.vue'
                    ),
            },
        ],
    },
    {
        path: '/user',
        component: () => import('@/layouts/default/DefaultLayout.vue'),
        children: [
            {
                path: '',
                name: 'User',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/UserView.vue'
                    ),
            },
        ],
    },
    {
        path: '/address',
        component: () => import('@/layouts/default/DefaultLayout.vue'),
        children: [
            {
                path: '',
                name: 'Address',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/AddressView.vue'
                    ),
            },
        ],
    },
    {
        path: '/dish',
        component: () => import('@/layouts/default/DefaultLayout.vue'),
        children: [
            {
                path: '',
                name: 'Dish',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/DishView.vue'
                    ),
            },
        ],
    },
    {
        path: '/offer',
        component: () => import('@/layouts/default/DefaultLayout.vue'),
        children: [
            {
                path: '',
                name: 'Offer',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/OfferView.vue'
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
