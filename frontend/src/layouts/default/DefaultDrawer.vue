<script setup>
import { ref } from 'vue'
import { useAppStore } from '@/store/app'

const appStore = useAppStore()

const items = ref([
    {
        title: 'Address',
        to: '/address',
        icon: 'mdi-map',
    },
    {
        title: 'User',
        to: '/user',
        icon: 'mdi-account',
    },
])
</script>

<template>
    <v-navigation-drawer
        v-model="appStore.drawer"
        temporary
    >
        <v-list
            dense
            shaped
        >
            <v-list-item
                v-for="item in items"
                :key="item.title"
                link
                :to="item.to"
            >
                <template v-slot:prepend>
                    <v-icon>{{ item.icon }}</v-icon>
                </template>

                <v-list-item-title>
                    {{ item.title }}
                </v-list-item-title>
            </v-list-item>
        </v-list>
    </v-navigation-drawer>
</template>
