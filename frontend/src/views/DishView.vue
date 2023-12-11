<script setup>
import { ref, onMounted } from 'vue'
import { addDish, deleteDish, readDishes } from '@/api'

const name = ref('')
const isVegetarian = ref(false)
const description = ref('')
const price = ref('')
const howManyDaysBeforeExpiration = ref('')

const dishes = ref([])

onMounted(async () => {
    dishes.value = await readDishes()
})

const dishPreviews = (dish) => ({
    title: `${dish.name} (${dish.price})`,
})

const submit = async () => {
    await addDish(
        name.value,
        isVegetarian.value,
        description.value,
        parseInt(price.value),
        parseInt(howManyDaysBeforeExpiration.value)
    )

    dishes.value = await readDishes()
}

const dishToRemove = ref(null)

const remove = async () => {
    await deleteDish(dishToRemove.value.id)

    dishes.value = await readDishes()
    dishToRemove.value = null
}
</script>

<template>
    <v-container class="fill-height">
        <v-responsive class="align-center text-center fill-height">
            <h1 class="text-h4">Add dish</h1>

            <v-text-field
                v-model="name"
                label="Name"
                required
                hide-details
            ></v-text-field>
            <v-checkbox
                v-model="isVegetarian"
                label="Is vegetarian"
            ></v-checkbox>
            <v-text-field
                v-model="description"
                label="Description"
                required
                hide-details
            ></v-text-field>
            <v-text-field
                v-model="price"
                label="Price"
                required
                hide-details
            ></v-text-field>
            <v-text-field
                v-model="howManyDaysBeforeExpiration"
                label="How many days before expiration"
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

                Add dish
            </v-btn>

            <h1 class="text-h4">Dishes</h1>

            <div>{{ JSON.stringify(dishes) }}</div>

            <h1 class="text-h4">Remove dish</h1>

            <v-select
                v-model="dishToRemove"
                label="Dish to remove"
                :items="dishes"
                :item-props="dishPreviews"
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

                Remove dish
            </v-btn>
        </v-responsive>
    </v-container>
</template>
