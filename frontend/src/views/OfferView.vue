<script setup>
import { ref, onMounted } from 'vue'
import {
    addOffer,
    deleteOffer,
    readAddresses,
    readDishes,
    readOffers,
    readUsers,
} from '@/api'

const dish = ref(null)
const seller = ref(null)
const address = ref(null)

const dishes = ref([])
const users = ref([])
const addresses = ref([])

const offers = ref([])

onMounted(async () => {
    dishes.value = await readDishes()
    users.value = await readUsers()
    addresses.value = await readAddresses()
    offers.value = await readOffers()
})

const dishPreviews = (dish) => ({
    title: `${dish.name} (${dish.price})`,
})
const addressPreviews = (address) => ({
    title: `${address.city}, ${address.streetName}, ${address.houseNr}-${address.apartamentNr}`,
})
const userPreviews = (user) => ({
    title: `${user.name} ${user.surname}`,
})
const offerPreviews = (offer) => {
    const previewSeller = users.value.find((user) => user.id === offer.sellerId)
    const previewDish = dishes.value.find((dish) => dish.id === offer.dishId)

    return {
        title: `${previewSeller.name} ${previewSeller.surname}, ${previewDish.name}`,
    }
}

const submit = async () => {
    await addOffer(dish.value.id, seller.value.id, address.value.id)

    offers.value = await readOffers()
}

const offerToRemove = ref(null)

const remove = async () => {
    await deleteOffer(offerToRemove.value.id)

    offers.value = await readOffers()
    offerToRemove.value = null
}
</script>

<template>
    <v-container class="fill-height">
        <v-responsive class="align-center text-center fill-height">
            <h1 class="text-h4">Add offer</h1>

            <v-select
                v-model="dish"
                label="Dish"
                :items="dishes"
                :item-props="dishPreviews"
            ></v-select>
            <v-select
                v-model="seller"
                label="Seller"
                :items="users"
                :item-props="userPreviews"
            ></v-select>
            <v-select
                v-model="address"
                label="Address"
                :items="addresses"
                :item-props="addressPreviews"
            ></v-select>

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

                Add offers
            </v-btn>

            <h1 class="text-h4">Offers</h1>

            <div>{{ JSON.stringify(offers) }}</div>

            <h1 class="text-h4">Remove offer</h1>

            <v-select
                v-model="offerToRemove"
                label="Offer to remove"
                :items="offers"
                :item-props="offerPreviews"
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

                Remove offer
            </v-btn>
        </v-responsive>
    </v-container>
</template>
