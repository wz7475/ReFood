<script setup>
import { ref } from 'vue'
import { addUser } from '@/api'
//add_user(name, surname, age, address_id, phone_nr, rating):
const name = ref('')
const surname = ref('')
const age = ref('')
const addressId = ref(0)
const phoneNr = ref('')
const rating = ref('')

const submit = async () => {
    await addUser(
        name.value,
        surname.value,
        parseInt(age.value),
        addressId.value,
        phoneNr.value,
        rating.value
    )
}
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
        </v-responsive>
    </v-container>
</template>
