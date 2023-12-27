import { apiFetch } from '.'
import { transformOffer } from './transformOffer'

export const searchOffers = async (searchText) => {
    return await apiFetch(`offers_filter/${searchText}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
    }).then((offers) => offers.map((offer) => transformOffer(offer)))
}
