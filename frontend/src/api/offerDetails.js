import { apiFetch } from '.'
import { transformOffer } from './transformOffer'

export const offerDetails = async (id) => {
    return await apiFetch(`offers/${id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(([offer]) => transformOffer(offer))
}
