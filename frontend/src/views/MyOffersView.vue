<script setup>
import { ref } from 'vue'

const status = ref('open')
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
                v-model="status"
                fixed-tabs
            >
                <v-tab value="open">Open</v-tab>
                <v-tab value="reserved">Reserved</v-tab>
                <v-tab value="completed">Completed</v-tab>
            </v-tabs>
        </v-sheet>
    </v-responsive>
</template>
