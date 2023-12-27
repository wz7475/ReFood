<script setup>
import { useAppStore } from '@/store/app'

const appStore = useAppStore()

const props = defineProps(['items'])
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
                v-for="item in props.items"
                :key="item.title"
                link
                :to="item.to"
                @click="item.action"
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
