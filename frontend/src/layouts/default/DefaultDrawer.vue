<script setup>
import { useAppStore } from '@/store/app'

const appStore = useAppStore()
</script>

<template>
    <v-navigation-drawer
        v-model="appStore.drawer"
        temporary
    >
        <v-list :items="items"></v-list>
    </v-navigation-drawer>
</template>
