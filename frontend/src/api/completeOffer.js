import { apiFetch } from '.'

export const completeOffer = async (id) => {
    return await apiFetch(`complete_offer/${id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
}
