<script setup>
import OfferSearchBar from '@/components/OfferSearchBar.vue'
import { ref } from 'vue'

const results = ref([
    {
        id: 1,
        distance: 123.4,
        price: 15.0,
        dishName: 'Pierogi',
        sellerName: 'Kuba Zszywacz',
        tags: ['sugarFree', 'vege'],
    },
    {
        id: 2,
        distance: 50.1,
        price: 100.0,
        dishName: 'Barszcz',
        sellerName: 'Jan Dziurkacz',
        tags: ['glutenFree'],
    },
    {
        id: 3,
        distance: 1.1,
        price: 1.0,
        dishName: 'Spaghetti',
        sellerName: 'Andrzej Pożar',
        tags: ['spicy'],
    },
    {
        id: 4,
        distance: 0.5,
        price: 0.1,
        dishName: 'Woda',
        sellerName: 'Kuba Rozpruwacz',
        tags: ['sugarFree', 'vege', 'spicy', 'glutenFree'],
    },
])

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
