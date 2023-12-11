// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

import colors from 'vuetify/util/colors'

export default createVuetify({
    theme: {
        themes: {
            light: {
                colors: {
                    primary: colors.green.base,
                    secondary: colors.purple.base,
                },
            },
        },
    },
})
