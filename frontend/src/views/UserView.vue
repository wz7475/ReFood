<script setup>
import { ref, onMounted } from 'vue'
import { addUser, readUsers, readAddresses } from '@/api'

const name = ref('')
const surname = ref('')
const age = ref('')
const address = ref(null)
const phoneNr = ref('')
const rating = ref('')

const users = ref([])
const addresses = ref([])

const submit = async () => {
    await addUser(
        name.value,
        surname.value,
        parseInt(age.value),
        address.value.id,
        phoneNr.value,
        rating.value
    )

    users.value = await readUsers()
}

onMounted(async () => {
    addresses.value = await readAddresses()
    users.value = await readUsers()
})

const addressPreviews = (address) => ({
    title: `${address.city}, ${address.streetName}, ${address.houseNr}-${address.apartamentNr}`,
})
</script>

<template>
    <v-container class="fill-height">
        <v-responsive class="align-center text-center fill-height">
            <h1 class="text-h4">Add user</h1>

            <v-text-field
                v-model="name"
                label="First name"
                required
                hide-details
            ></v-text-field>
            <v-text-field
                v-model="surname"
                label="Surname"
                required
                hide-details
            ></v-text-field>

            <v-select
                v-model="address"
                label="Address"
                :items="addresses"
                :item-props="addressPreviews"
            ></v-select>

            <v-text-field
                v-model="age"
                label="Age"
                required
                hide-details
            ></v-text-field>
            <v-text-field
                v-model="phoneNr"
                label="Phone number"
                required
                hide-details
            ></v-text-field>
            <v-text-field
                v-model="rating"
                label="Rating"
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

                Add user
            </v-btn>

            <h1 class="text-h4">Users</h1>

            <div>{{ JSON.stringify(users) }}</div>
        </v-responsive>
    </v-container>
</template>
