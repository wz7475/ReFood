import { apiFetch } from '.'
import { transformOffer } from './transformOffer'

export const myOffers = async () => {
    return await apiFetch('my_offers', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
    }).then((offers) => offers.map((offer) => transformOffer(offer)))
}
