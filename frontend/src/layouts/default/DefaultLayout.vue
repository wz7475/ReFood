<script setup>
import DefaultBar from './DefaultBar.vue'
import DefaultView from './DefaultView.vue'
import DefaultDrawer from './DefaultDrawer.vue'
import { useAppStore } from '@/store/app'
import { computed } from 'vue'

const appStore = useAppStore()

const items = computed(() =>
    !appStore.signedIn
        ? [
              {
                  title: 'Home',
                  to: '/home',
                  icon: 'mdi-home',
              },
              {
                  title: 'Register',
                  to: '/register',
                  icon: 'mdi-account-plus',
              },
              {
                  title: 'Login',
                  to: '/login',
                  icon: 'mdi-login',
              },
          ]
        : [
              {
                  title: 'Dashboard',
                  to: '/dashboard',
                  icon: 'mdi-view-dashboard',
              },
              {
                  title: 'Search offers',
                  to: '/search',
                  icon: 'mdi-magnify',
              },
              {
                  title: 'Add offer',
                  to: '/addOffer',
                  icon: 'mdi-plus-box',
              },
              {
                  title: 'My offers',
                  to: '/myOffers',
                  icon: 'mdi-food',
              },

              {
                  title: 'Log out',
                  action: appStore.logout,
                  to: '/home',
                  icon: 'mdi-logout',
              },
          ]
)
</script>

<template>
    <v-app>
        <DefaultBar />

        <DefaultView />

        <DefaultDrawer :items="items" />
    </v-app>
</template>
