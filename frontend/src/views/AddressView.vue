<script setup>
import { ref, onMounted } from 'vue'
import { addAddress, readAddresses } from '@/api'

const streetName = ref('')
const houseNr = ref('')
const apartamentNr = ref('')
const city = ref('')

const submit = async () => {
    await addAddress(
        streetName.value,
        parseInt(houseNr.value),
        parseInt(apartamentNr.value),
        city.value
    )

    addresses.value = await readAddresses()
}

const addresses = ref([])

onMounted(async () => {
    addresses.value = await readAddresses()
})
</script>

<template>
    <v-container class="fill-height">
        <v-responsive class="align-center text-center fill-height">
            <h1 class="text-h4">Add address</h1>

            <v-text-field
                v-model="streetName"
                label="Street name"
                required
                hide-details
            ></v-text-field>
            <v-text-field
                v-model="houseNr"
                label="House number"
                required
                hide-details
            ></v-text-field>
            <v-text-field
                v-model="apartamentNr"
                label="Apartament number"
                required
                hide-details
            ></v-text-field>
            <v-text-field
                v-model="city"
                label="City"
                required
                hide-details
            ></v-text-field>

            <div class="py-8" />

            <v-btn
                min-width="164"
                color="secondary"
                @click="submit"
            >
                <v-icon
                    icon="mdi-plus"
                    size="large"
                    start
                />

                Add address
            </v-btn>

            <h1 class="text-h4">Addresses</h1>

            <div>{{ JSON.stringify(addresses) }}</div>
        </v-responsive>
    </v-container>
</template>
