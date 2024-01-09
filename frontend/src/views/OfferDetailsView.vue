<script setup>
import { ref, onMounted } from 'vue'
import { LMap, LTileLayer, LMarker, LIcon } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-geosearch/assets/css/leaflet.css'
import defaultIcon from 'leaflet/dist/images/marker-icon.png'
import { offerDetails, reserveOffer, completeOffer } from '@/api'
import { useRoute } from 'vue-router'
const zoom = ref(10)
const map = ref(null)

const defaultPosition = ref({ lat: 52.02, lng: 19.2 })
const currentPosition = ref(null)

const onReady = (map) => {
    navigator.geolocation.getCurrentPosition((position) => {
        const lat = position.coords.latitude
        const lng = position.coords.longitude
        const margin = 0.01

        currentPosition.value = {
            lat,
            lng,
        }

        const latMin = Math.min(
            currentPosition.value.lat,
            result.value.latitude
        )
        const latMax = Math.max(
            currentPosition.value.lat,
            result.value.latitude
        )
        const lngMin = Math.min(
            currentPosition.value.lng,
            result.value.longitude
        )
        const lngMax = Math.max(
            currentPosition.value.lng,
            result.value.longitude
        )

        map.fitBounds([
            [latMin - margin, lngMin - margin],
            [latMax + margin, lngMax + margin],
        ])
    })
}

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

const result = ref(null)

const route = useRoute()

onMounted(async () => {
    result.value = await offerDetails(route.params.id)
})

const doReserve = async () => {
    await reserveOffer(result.value.id)
    result.value = await offerDetails(route.params.id)
}
const doComplete = async () => {
    await completeOffer(result.value.id)
    result.value = await offerDetails(route.params.id)
}
</script>

<template>
    <v-responsive class="align-center text-center fill-height">
        <v-card
            v-if="result"
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
                            (currentPosition &&
                                (currentPosition.lat + result.latitude) / 2) ||
                                result.latitude ||
                                defaultPosition.lat,
                            (currentPosition &&
                                (currentPosition.lng + result.longitude) / 2) ||
                                result.longitude ||
                                defaultPosition.lng,
                        ]"
                        :useGlobalLeaflet="false"
                        @ready="onReady"
                    >
                        <l-tile-layer
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                            layer-type="base"
                            name="OpenStreetMap"
                        ></l-tile-layer>

                        <l-marker
                            visible
                            :lat-lng="{
                                lat: result.latitude || 0.0,
                                lng: result.longitude || 0.0,
                            }"
                        ></l-marker>

                        <l-marker
                            v-if="currentPosition"
                            visible
                            v-model:lat-lng="currentPosition"
                        >
                            <l-icon
                                :icon-url="defaultIcon"
                                :iconSize="[25, 41]"
                                :iconAnchor="[12, 41]"
                                :popupAnchor="[1, -34]"
                                :tooltipAnchor="[16, -28]"
                                :shadowSize="[41, 41]"
                                class-name="currentLocMarker"
                            ></l-icon>
                        </l-marker>
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
                    v-if="result.state === 'open'"
                    color="secondary"
                    block
                    variant="elevated"
                    rounded="xl"
                    prepend-icon="mdi-chevron-left"
                    append-icon="mdi-chevron-right"
                    @click="doReserve"
                >
                    Reserve
                </v-btn>
                <v-btn
                    v-if="result.state === 'reserved'"
                    color="green"
                    block
                    variant="elevated"
                    rounded="xl"
                    prepend-icon="mdi-chevron-left"
                    append-icon="mdi-chevron-right"
                    @click="doComplete"
                >
                    Confirm
                </v-btn>
                <v-btn
                    v-if="result.state === 'complete'"
                    color="grey"
                    block
                    variant="elevated"
                    rounded="xl"
                    prepend-icon="mdi-chevron-left"
                    append-icon="mdi-chevron-right"
                >
                    Order complete
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-responsive>
</template>

<style>
.currentLocMarker {
    filter: hue-rotate(120deg);
}
</style>
