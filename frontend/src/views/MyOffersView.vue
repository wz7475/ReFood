<script setup>
import { myOffers } from '@/api'
import { computed } from 'vue'
import { ref, onMounted } from 'vue'

const status = ref('open')

const data = ref([])
const results = computed(() =>
    data.value.filter((offer) => offer.state === status.value)
)

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

onMounted(async () => {
    data.value = await myOffers()
})
</script>

<template>
    <div class="align-center text-center fill-height">
        <v-sheet
            :elevation="4"
            max-width="500"
            rounded
            class="align-center justify-center mx-auto pa-4 flex-column flex-grow-1"
        >
            <v-tabs
                v-model="status"
                fixed-tabs
            >
                <v-tab value="open">Open</v-tab>
                <v-tab value="reserved">Reserved</v-tab>
                <v-tab value="complete">Completed</v-tab>
            </v-tabs>

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

                    <v-card-subtitle>{{ result.distance }}km</v-card-subtitle>
                    <v-card-text>
                        <p v-if="result.sellerName">
                            Seller: {{ result.sellerName }}
                        </p>
                        <p v-if="result.buyerName">
                            Buyer: {{ result.buyerName }}
                        </p>
                    </v-card-text>

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
                        :to="{
                            name: 'offerDetails',
                            params: { id: result.id },
                        }"
                        append-icon="mdi-chevron-right"
                    >
                        Details
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-sheet>
    </div>
</template>
