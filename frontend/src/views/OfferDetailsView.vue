<script setup>
import { ref } from 'vue'
import { LMap, LTileLayer, LMarker } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-geosearch/assets/css/leaflet.css'
const zoom = ref(6)
const map = ref(null)

const position = ref({ lat: 52.0, lng: 20.0 })
const defaultPosition = ref({ lat: 52.02, lng: 19.2 })

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

const result = {
    id: 4,
    distance: 0.5,
    price: 0.1,
    dishName: 'Woda',
    sellerName: 'Kuba Rozpruwacz',
    tags: ['sugarFree', 'vege', 'spicy', 'glutenFree'],
    description: 'Extremely refreshing drink suitable for all consumers',
}
</script>

<template>
    <v-responsive class="align-center text-center fill-height">
        <v-card
            class="text-left mx-auto my-4"
            max-width="1000"
        >
            <v-card-item>
                <v-card-title class="d-flex flex-row">
                    {{ result.dishName }}
                    <v-spacer />
                    {{ result.price }}zł
                </v-card-title>

                <v-card-subtitle>{{ result.distance }}km</v-card-subtitle>

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

                <div
                    :style="{ height: '50vh', 'max-width': '1000px' }"
                    class="ma-auto py-4"
                >
                    <l-map
                        v-model:zoom="zoom"
                        ref="map"
                        :center="[
                            position.lat || defaultPosition.lat,
                            position.lng || defaultPosition.lng,
                        ]"
                        :useGlobalLeaflet="false"
                    >
                        <l-tile-layer
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                            layer-type="base"
                            name="OpenStreetMap"
                        ></l-tile-layer>

                        <l-marker
                            visible
                            :lat-lng="position"
                        ></l-marker>
                    </l-map>
                </div>

                <v-card-text
                    :style="{ 'max-width': '500px' }"
                    class="ma-auto"
                >
                    <p v-if="result.sellerName">
                        Seller: {{ result.sellerName }}
                    </p>
                    <p v-if="result.buyerName">Buyer: {{ result.buyerName }}</p>
                    <div class="py-4">
                        Description:
                        <p>
                            {{ result.description }}
                        </p>
                    </div>
                </v-card-text>
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
