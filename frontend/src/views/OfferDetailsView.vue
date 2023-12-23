<script setup>
import { ref } from 'vue'
import { LMap, LTileLayer, LMarker } from '@vue-leaflet/vue-leaflet'
import { GeoSearchControl, OpenStreetMapProvider } from 'leaflet-geosearch'
import 'leaflet/dist/leaflet.css'
import 'leaflet-geosearch/assets/css/leaflet.css'
const zoom = ref(6)
const map = ref(null)

// 6 {"lat":52.01902669262724,"lng":19.204101562500004}

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
</script>

<template>
    <v-responsive class="align-center text-center fill-height">
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
        {{ zoom }}
        {{ JSON.stringify(position) }}
    </v-responsive>
</template>
