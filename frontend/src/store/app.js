// Utilities
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAppStore = defineStore('app', () => {
    const drawer = ref(false)
    const signedIn = ref(true)

    const logout = () => {
        signedIn.value = false
    }

    return {
        drawer,
        signedIn,
        logout,
    }
})
