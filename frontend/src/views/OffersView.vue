<script setup>
import { searchOffers } from '@/api'
import OfferSearchBar from '@/components/OfferSearchBar.vue'
import { computed } from 'vue'
import { watch } from 'vue'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()

const data = ref([])

const chipConfig = {
    vege: { text: 'Vege', color: 'green', icon: 'mdi-sprout' },
    spicy: { text: 'Spicy', color: 'red', icon: 'mdi-fire' },
    glutenFree: {
        text: 'Gluten free',
        color: 'yellow',
        icon: 'mdi-barley-off',
    },
    sugarFree: {
        text: 'Sugar free',
        color: 'light-blue',
        icon: 'mdi-cube-off-outline',
    },
}

const results = computed(() => data.value)

const getResult = async () => {
    data.value = []
    const tags = JSON.parse(route.query.options || '[]').map((tag) =>
        Object.keys(chipConfig).indexOf(tag)
    )
    const lat = parseFloat(route.query.lat || '0.0')
    const lon = parseFloat(route.query.lon || '0.0')
    const distance = parseFloat(route.query.distance || '100000.0')
    data.value = await searchOffers(
        route.params.query,
        tags,
        distance,
        lat,
        lon
    )
}

watch(route, getResult)

onMounted(getResult)
</script>

<template>
    <v-responsive class="align-center text-center fill-height">
        <OfferSearchBar />

        <v-card
            v-for="result in results"
            v-bind:key="result.id"
            class="text-left mx-auto my-4"
            max-width="700"
        >
            <v-card-item>
                <v-card-title class="d-flex flex-row">
                    {{ result.dishName }}
                    <v-spacer />
                    {{ result.price }}zł
                </v-card-title>

                <v-card-subtitle>
                    {{ result.distance }}km - {{ result.sellerName }}
                </v-card-subtitle>

                <div class="d-flex flex-row ga-1">
                    <v-chip
                        v-for="tag in result.tags"
                        :key="tag"
                        :color="chipConfig[tag].color"
                        variant="flat"
                    >
                        <v-icon
                            start
                            :icon="chipConfig[tag].icon"
                        ></v-icon>
                        {{ chipConfig[tag].text }}
                    </v-chip>
                </div>
            </v-card-item>

            <v-card-actions>
                <v-spacer />
                <v-btn
                    color="secondary"
                    :to="{ name: 'offerDetails', params: { id: result.id } }"
                    append-icon="mdi-chevron-right"
                >
                    Details
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-responsive>
</template>
