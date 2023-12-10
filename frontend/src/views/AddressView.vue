<script setup>
import { ref, onMounted } from 'vue'
import { addAddress, deleteAddress, readAddresses } from '@/api'

const streetName = ref('')
const houseNr = ref('')
const apartamentNr = ref('')
const city = ref('')

const addresses = ref([])

onMounted(async () => {
    addresses.value = await readAddresses()
})

const addressPreviews = (address) => ({
    title: `${address.city}, ${address.streetName}, ${address.houseNr}-${address.apartamentNr}`,
})

const submit = async () => {
    await addAddress(
        streetName.value,
        parseInt(houseNr.value),
        parseInt(apartamentNr.value),
        city.value
    )

    addresses.value = await readAddresses()
}

const addressToRemove = ref(null)

const remove = async () => {
    await deleteAddress(addressToRemove.value.id)

    addresses.value = await readAddresses()
    addressToRemove.value = null
}
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

            <h1 class="text-h4">Remove address</h1>

            <v-select
                v-model="addressToRemove"
                label="Address to remove"
                :items="addresses"
                :item-props="addressPreviews"
            ></v-select>
            <v-btn
                min-width="164"
                color="red"
                @click="remove"
            >
                <v-icon
                    icon="mdi-delete"
                    size="large"
                    start
                />

                Remove address
            </v-btn>
        </v-responsive>
    </v-container>
</template>
