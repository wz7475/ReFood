import { apiFetch } from '.'

export const reserveOffer = async (id) => {
    return await apiFetch('offers/reserve', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },

        body: JSON.stringify(id),
    })
}
