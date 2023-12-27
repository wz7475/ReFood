<script setup>
import { computed } from 'vue'
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
const router = useRouter()
const route = useRoute()

const query = ref(route.params.query || '')

const initialOptions = computed(() => JSON.parse(route.query.options || '[]'))

const vege = ref(initialOptions.value.includes('vege'))
const spicy = ref(initialOptions.value.includes('spicy'))
const glutenFree = ref(initialOptions.value.includes('glutenFree'))
const sugarFree = ref(initialOptions.value.includes('sugarFree'))

const submit = () => {
    const options = []

    if (vege.value) options.push('vege')
    if (spicy.value) options.push('spicy')
    if (glutenFree.value) options.push('glutenFree')
    if (sugarFree.value) options.push('sugarFree')

    router.push({
        name: 'offers',
        params: {
            query: query.value,
        },
        query: {
            options: JSON.stringify(options),
        },
    })
}
</script>
<template>
    <div>
        <div
            :style="{ 'max-width': '500px' }"
            class="d-flex flex-row ma-auto my-2"
        >
            <v-text-field
                v-model="query"
                class="flex-full-width mr-2"
                density="comfortable"
                placeholder="Search offers"
                prepend-inner-icon="mdi-magnify"
                rounded
                theme="light"
                variant="solo"
                hide-details
                @keyup.enter="submit"
            ></v-text-field>

            <v-btn
                density="default"
                icon="mdi-arrow-right"
                color="secondary"
                @click="submit"
            ></v-btn>
        </div>

        <div
            :style="{ 'max-width': '500px' }"
            class="d-flex flex-row ma-auto ga-1 px-4"
        >
            <v-chip
                link
                :color="vege ? 'green' : 'default'"
                :variant="vege ? 'flat' : 'plain'"
                @click="vege = !vege"
            >
                <v-icon
                    start
                    icon="mdi-sprout"
                ></v-icon>
                Vege
            </v-chip>
            <v-chip
                link
                :color="spicy ? 'red' : 'default'"
                :variant="spicy ? 'flat' : 'plain'"
                @click="spicy = !spicy"
            >
                <v-icon
                    start
                    icon="mdi-fire"
                ></v-icon>
                Spicy
            </v-chip>
            <v-chip
                link
                :color="glutenFree ? 'yellow' : 'default'"
                :variant="glutenFree ? 'flat' : 'plain'"
                @click="glutenFree = !glutenFree"
            >
                <v-icon
                    start
                    icon="mdi-barley-off"
                ></v-icon>
                Gluten free
            </v-chip>
            <v-chip
                link
                :color="sugarFree ? 'light-blue' : 'default'"
                :variant="sugarFree ? 'flat' : 'plain'"
                @click="sugarFree = !sugarFree"
            >
                <v-icon
                    start
                    icon="mdi-cube-off-outline"
                ></v-icon>
                Sugar free
            </v-chip>
        </div>
    </div>
</template>
