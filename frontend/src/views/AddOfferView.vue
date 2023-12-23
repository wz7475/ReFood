<script setup>
import { ref } from 'vue'
import { LMap, LTileLayer, LMarker } from '@vue-leaflet/vue-leaflet'
import { GeoSearchControl, OpenStreetMapProvider } from 'leaflet-geosearch'
import 'leaflet/dist/leaflet.css'
import 'leaflet-geosearch/assets/css/leaflet.css'
const zoom = ref(6)
const map = ref(null)

const position = ref({ lat: null, lng: null })
const defaultPosition = ref({ lat: 52.02, lng: 19.2 })

const onMapClick = (value) => {
    position.value = value.latlng
}

const onReady = (map) => {
    map.doubleClickZoom.disable()

    const search = new GeoSearchControl({
        provider: new OpenStreetMapProvider(),
        retainZoomLevel: true,
        showMarker: false,
        showPopup: false,
        keepResult: false,
        autoClose: true,
        style: 'bar',
    })

    map.addControl(search)

    map.on('geosearch/showlocation', (val) => {
        position.value = { lat: val.location.y, lng: val.location.x }
        console.log(val.location, val.location.bounds)
        map.fitBounds(val.location.bounds)
    })
}

const vege = ref(false)
const spicy = ref(false)
const glutenFree = ref(false)
const sugarFree = ref(false)

const submit = () => {}
</script>

<template>
    <v-responsive class="align-center text-center fill-height pt-2 pb-8">
        <div
            :style="{ height: '50vh', 'max-width': '1000px' }"
            class="ma-auto"
        >
            <l-map
                v-model:zoom="zoom"
                ref="map"
                :center="[
                    position.lat || defaultPosition.lat,
                    position.lng || defaultPosition.lng,
                ]"
                :useGlobalLeaflet="false"
                @dblclick="onMapClick"
                @ready="onReady"
            >
                <l-tile-layer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    layer-type="base"
                    name="OpenStreetMap"
                ></l-tile-layer>

                <l-marker
                    v-if="position.lat && position.lng"
                    visible
                    draggable
                    v-model:lat-lng="position"
                    @dragstart="dragging = true"
                    @dragend="dragging = false"
                ></l-marker>
            </l-map>
        </div>
        <div
            :style="{ 'max-width': '500px' }"
            class="ma-auto"
        >
            <v-text-field
                v-model="login"
                label="Dish name"
                required
                hide-details
                class="ma-2"
            />
            <v-textarea
                v-model="login"
                label="Description"
                required
                hide-details
                class="ma-2"
            />
            <v-text-field
                v-model="login"
                label="Price"
                suffix="zł"
                required
                hide-details
                class="ma-2"
            />

            <div class="d-flex flex-row justify-center ma-auto ga-1 py-2">
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

            <v-btn
                class="w-100"
                color="secondary"
                @click="submit"
            >
                <v-icon
                    icon="mdi-plus-box"
                    size="large"
                    start
                />

                Add offer
            </v-btn>
        </div>
    </v-responsive>
</template>
