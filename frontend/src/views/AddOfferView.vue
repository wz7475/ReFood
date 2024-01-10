<script setup>
import { ref, watch, computed } from 'vue'
import { LMap, LTileLayer, LMarker, LIcon } from '@vue-leaflet/vue-leaflet'
import { GeoSearchControl, OpenStreetMapProvider } from 'leaflet-geosearch'
import 'leaflet/dist/leaflet.css'
import 'leaflet-geosearch/assets/css/leaflet.css'
import defaultIcon from 'leaflet/dist/images/marker-icon.png'
import { addOffer } from '@/api'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/store/app'
const zoom = ref(6)
const mapRef = ref(null)

const appStore = useAppStore()

const position = ref({ lat: null, lng: null })
const defaultPosition = computed(() => ({
    lat: appStore.currentPosition.latitude,
    lng: appStore.currentPosition.longitude,
}))

const onMapClick = (value) => {
    position.value = value.latlng
}

const fitBounds = () => {
    const lat = appStore.currentPosition.latitude
    const lng = appStore.currentPosition.longitude
    const margin = 0.01

    mapRef.value.fitBounds([
        [lat - margin, lng - margin],
        [lat + margin, lng + margin],
    ])
}

const onReady = (map) => {
    mapRef.value = map
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
        map.fitBounds(val.location.bounds)
        console.log(val.location.bounds)
    })

    fitBounds()
}

watch(defaultPosition, fitBounds)

const vege = ref(false)
const spicy = ref(false)
const glutenFree = ref(false)
const sugarFree = ref(false)

const dishName = ref('')
const description = ref('')
const price = ref('')

const router = useRouter()

const submit = async () => {
    const tags = []
    if (vege.value) tags.push(0)
    if (spicy.value) tags.push(1)
    if (glutenFree.value) tags.push(2)
    if (sugarFree.value) tags.push(3)

    const offerId = await addOffer(
        position.value.lat,
        position.value.lng,
        dishName.value,
        description.value,
        parseFloat(price.value),
        tags
    )

    router.push({
        name: 'offerDetails',
        params: {
            id: offerId,
        },
    })
}
</script>

<template>
    <v-responsive class="align-center text-center fill-height pt-2 pb-8">
        <div
            :style="{ height: '50vh', 'max-width': '1000px' }"
            class="ma-auto"
        >
            <l-map
                v-model:zoom="zoom"
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
                ></l-marker>

                <l-marker
                    visible
                    v-model:lat-lng="defaultPosition"
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
        <div
            :style="{ 'max-width': '500px' }"
            class="ma-auto"
        >
            <v-text-field
                v-model="dishName"
                label="Dish name"
                required
                hide-details
                class="ma-2"
                @keyup.enter="submit"
            />
            <v-textarea
                v-model="description"
                label="Description"
                required
                hide-details
                class="ma-2"
            />
            <v-text-field
                v-model="price"
                label="Price"
                suffix="zł"
                required
                hide-details
                class="ma-2"
                @keyup.enter="submit"
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
<style>
.currentLocMarker {
    filter: hue-rotate(120deg);
}
</style>
