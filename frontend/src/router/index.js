// Composables
import { createRouter, createWebHistory } from 'vue-router'
import { useAppStore } from '@/store/app'

const routes = [
    {
        path: '/',
        component: () => import('@/layouts/default/DefaultLayout.vue'),
        children: [
            {
                path: '/',
                redirect: { name: 'home' },
                meta: { requiresAuth: false },
            },
            {
                path: '/home',
                name: 'home',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/HomeView.vue'
                    ),
                meta: { requiresAuth: false },
            },
            {
                path: '/login',
                name: 'login',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/LoginView.vue'
                    ),
                meta: { requiresAuth: false },
            },
            {
                path: '/register',
                name: 'register',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/LoginView.vue'
                    ),
                meta: { requiresAuth: false },
            },

            {
                path: '/dashboard',
                name: 'dashboard',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/DashboardView.vue'
                    ),
                meta: { requiresAuth: true },
            },
            {
                path: '/search',
                name: 'search',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/SearchView.vue'
                    ),
                meta: { requiresAuth: true },
            },
            {
                path: '/offers/:query',
                name: 'offers',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/OffersView.vue'
                    ),
                meta: { requiresAuth: true },
            },
            {
                path: '/offer/:id',
                name: 'offerDetails',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/OfferDetailsView.vue'
                    ),
                meta: { requiresAuth: true },
            },
            {
                path: '/addOffer',
                name: 'addOffer',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/AddOfferView.vue'
                    ),
                meta: { requiresAuth: true },
            },
            {
                path: '/myOffers',
                name: 'myOffers',
                component: () =>
                    import(
                        /* webpackChunkName: "home" */ '@/views/MyOffersView.vue'
                    ),
                meta: { requiresAuth: true },
            },
        ],
    },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
})

router.beforeEach((to) => {
    const appStore = useAppStore()

    if (to.meta.requiresAuth && !appStore.signedIn) {
        return {
            name: 'login',
        }
    }
})

export default router
