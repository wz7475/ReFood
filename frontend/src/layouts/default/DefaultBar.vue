<script setup>
import { useAppStore } from '@/store/app'

const appStore = useAppStore()
</script>

<template>
    <v-app-bar flat>
        <v-toolbar color="primary">
            <v-app-bar-nav-icon
                @click="appStore.drawer = true"
            ></v-app-bar-nav-icon>

            <v-toolbar-title>ReFood</v-toolbar-title>

            <v-spacer></v-spacer>

            <v-btn
                icon
                v-if="appStore.signedIn"
                @click="appStore.logout"
            >
                <v-icon>mdi-login</v-icon>
            </v-btn>
        </v-toolbar>
    </v-app-bar>
</template>
