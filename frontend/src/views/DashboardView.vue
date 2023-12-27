<script setup></script>

<template>
    <v-container class="fill-height">
        <v-responsive class="align-center text-center fill-height">
            <div class="text-body-2 font-weight-light mb-n1">Welcome to</div>

            <h1 class="text-h2 font-weight-bold">ReFood</h1>

            <div class="py-14" />

            <v-row class="d-flex align-center justify-center">
                <v-col cols="auto">
                    <v-btn
                        min-width="164"
                        variant="text"
                        to="/myOffers"
                    >
                        <v-icon
                            icon="mdi-food"
                            size="large"
                            start
                        />

                        My offers
                    </v-btn>
                </v-col>

                <v-col cols="auto">
                    <v-btn
                        color="primary"
                        min-width="228"
                        size="x-large"
                        variant="flat"
                        to="/search"
                    >
                        <v-icon
                            icon="mdi-magnify"
                            size="large"
                            start
                        />

                        Search offers
                    </v-btn>
                </v-col>

                <v-col cols="auto">
                    <v-btn
                        min-width="164"
                        variant="text"
                        to="/addOffer"
                    >
                        <v-icon
                            icon="mdi-plus-box"
                            size="large"
                            start
                        />

                        Add offer
                    </v-btn>
                </v-col>
            </v-row>
        </v-responsive>
    </v-container>
</template>
