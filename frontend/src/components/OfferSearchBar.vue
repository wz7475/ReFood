<script setup>
import { LMap, LTileLayer, LMarker, LIcon } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-geosearch/assets/css/leaflet.css'
import defaultIcon from 'leaflet/dist/images/marker-icon.png'
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppStore } from '@/store/app'
const router = useRouter()
const route = useRoute()
const appStore = useAppStore()

const currentPosition = computed({
    get() {
        return {
            lat: appStore.currentPosition.latitude,
            lng: appStore.currentPosition.longitude,
        }
    },

    set(newVal) {
        appStore.currentPosition = {
            latitude: newVal.lat,
            longitude: newVal.lng,
        }
    },
})

const query = ref(route.params.query || '')

const initialOptions = computed(() => JSON.parse(route.query.options || '[]'))

const vege = ref(initialOptions.value.includes('vege'))
const spicy = ref(initialOptions.value.includes('spicy'))
const glutenFree = ref(initialOptions.value.includes('glutenFree'))
const sugarFree = ref(initialOptions.value.includes('sugarFree'))

const distance = ref(50.0)
const useDistance = ref(false)

const zoom = ref(6)

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
            distance: useDistance.value ? distance.value : -1,
            lat: appStore.currentPosition.latitude,
            lon: appStore.currentPosition.longitude,
        },
    })
}
</script>
<template>
    <div>
        <div
            :style="{ height: '50vh', 'max-width': '1000px' }"
            class="ma-auto"
        >
            <l-map
                v-model:zoom="zoom"
                :center="[currentPosition.lat, currentPosition.lng]"
                :useGlobalLeaflet="false"
            >
                <l-tile-layer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    layer-type="base"
                    name="OpenStreetMap"
                ></l-tile-layer>

                <l-marker
                    draggable
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
        <div
            :style="{ 'max-width': '450px' }"
            class="d-flex flex-row ma-auto"
        >
            <v-checkbox-btn
                class="flex-grow-0"
                v-model="useDistance"
            ></v-checkbox-btn>
            <v-slider
                class="py-2"
                min="1"
                max="100"
                step="0.1"
                label="Distance"
                thumb-label
                v-model="distance"
                hide-details
            >
                <template v-slot:thumb-label="{ modelValue }">
                    {{ modelValue }}km
                </template>
            </v-slider>
        </div>
    </div>
</template>
<style>
.currentLocMarker {
    filter: hue-rotate(120deg);
}
</style>
