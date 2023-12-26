<script setup>
import { useAppStore } from '@/store/app'
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { login, register } from '@/api'
const route = useRoute()
const router = useRouter()
const appStore = useAppStore()

const isRegister = computed({
    get() {
        return route.name === 'register'
    },
    set(newVal) {
        router.push({ name: newVal ? 'register' : 'login' })
    },
})

const loginVal = ref('')
const name = ref('')
const surname = ref('')
const phoneNumber = ref('')
const password = ref('')
const confirmPassword = ref('')

const submitLogin = async () => {
    await login(loginVal.value, password.value)

    appStore.signedIn = true
    router.push({ name: 'dashboard' })
}
const submitRegister = async () => {
    if (password.value !== confirmPassword.value) return

    await register(
        name.value,
        surname.value,
        loginVal.value,
        password.value,
        phoneNumber.value
    )

    appStore.signedIn = true
    router.push({ name: 'dashboard' })
}
</script>

<template>
    <v-responsive class="align-center text-center fill-height">
        <v-sheet
            :elevation="4"
            max-width="500"
            rounded
            class="align-center justify-center mx-auto pa-4"
        >
            <v-tabs
                v-model="isRegister"
                fixed-tabs
            >
                <v-tab :value="true">Register</v-tab>
                <v-tab :value="false">Login</v-tab>
            </v-tabs>

            <v-text-field
                v-model="loginVal"
                label="Login"
                required
                hide-details
                class="ma-2"
            />
            <v-expand-transition>
                <v-text-field
                    v-show="isRegister"
                    v-model="name"
                    label="Name"
                    required
                    hide-details
                    class="ma-2"
                />
            </v-expand-transition>
            <v-expand-transition>
                <v-text-field
                    v-show="isRegister"
                    v-model="surname"
                    label="Surname"
                    required
                    hide-details
                    class="ma-2"
                />
            </v-expand-transition>
            <v-expand-transition>
                <v-text-field
                    v-show="isRegister"
                    v-model="phoneNumber"
                    label="Phone number"
                    required
                    hide-details
                    class="ma-2"
                />
            </v-expand-transition>

            <v-text-field
                v-model="password"
                label="Password"
                required
                hide-details
                class="ma-2"
            />
            <v-expand-transition>
                <v-text-field
                    v-show="isRegister"
                    v-model="confirmPassword"
                    label="Confirm password"
                    required
                    hide-details
                    class="ma-2"
                />
            </v-expand-transition>

            <v-expand-transition>
                <v-btn
                    v-show="isRegister"
                    class="w-100"
                    color="secondary"
                    @click="submitRegister"
                >
                    <v-icon
                        icon="mdi-account-plus"
                        size="large"
                        start
                    />

                    Register
                </v-btn>
            </v-expand-transition>
            <v-expand-transition>
                <v-btn
                    v-show="!isRegister"
                    class="w-100"
                    color="secondary"
                    @click="submitLogin"
                >
                    <v-icon
                        icon="mdi-login"
                        size="large"
                        start
                    />

                    Login
                </v-btn>
            </v-expand-transition>
        </v-sheet>
    </v-responsive>
</template>
