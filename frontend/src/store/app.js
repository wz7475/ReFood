// Utilities
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export const useAppStore = defineStore('app', () => {
    const router = useRouter()

    const drawer = ref(false)
    const signedIn = ref(
        document.cookie.match(/^(.*;)?\s*sessionId\s*=\s*[^;]+(.*)?$/)
    )

    const logout = () => {
        signedIn.value = false
        router.push({ name: 'home' })
    }

    return {
        drawer,
        signedIn,
        logout,
    }
})
