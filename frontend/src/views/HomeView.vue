<script setup></script>

<template>
    <v-container class="fill-height">
        <v-responsive class="align-center text-center fill-height">
            <div class="text-body-2 font-weight-light mb-n1">Welcome to</div>

            <h1 class="text-h2 font-weight-bold">ReFood</h1>

            <div class="py-14" />

            <v-btn
                color="primary"
                min-width="228"
                size="x-large"
                variant="flat"
                class="mb-8"
                to="/register"
            >
                <v-icon
                    icon="mdi-account-plus"
                    size="large"
                    start
                />

                Register
            </v-btn>
            <br />
            <v-btn
                min-width="164"
                variant="text"
                to="/login"
            >
                <v-icon
                    icon="mdi-login"
                    size="large"
                    start
                />

                Login
            </v-btn>
        </v-responsive>
    </v-container>
</template>
