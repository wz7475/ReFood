import { apiFetch } from '.'

export const completeOffer = async (id) => {
    return await apiFetch(`offers/complete/${id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
}
