<script setup>
import { useAppStore } from '@/store/app'
import { onMounted } from 'vue'

const appStore = useAppStore()

onMounted(() => {
    navigator.geolocation.getCurrentPosition((position) => {
        appStore.currentPosition = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
        }
    })
})
</script>

<template>
    <router-view />
</template>
