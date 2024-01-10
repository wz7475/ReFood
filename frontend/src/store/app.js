// Utilities
import { defineStore } from 'pinia'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

export const useAppStore = defineStore('app', () => {
    const router = useRouter()

    const drawer = ref(false)
    const signedIn = ref(
        document.cookie.match(/^(.*;)?\s*sessionId\s*=\s*[^;]+(.*)?$/)
    )

    const logout = () => {
        signedIn.value = false

        document.cookie =
            'sessionId' + '=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;'

        router.push({ name: 'home' })
    }

    const currentPosition = ref({ latitude: 52.02, longitude: 19.2 })

    return {
        drawer,
        signedIn,
        logout,
        currentPosition,
    }
})
