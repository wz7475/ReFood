import { apiFetch } from '.'
import { transformOffer } from './transformOffer'

export const searchOffers = async (searchText, tags, distance, lat, lon) => {
    return await apiFetch('offers/filter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            pattern: searchText,
            tags,
            distance,
            lat,
            lon,
        }),
    }).then((offers) => offers.map((offer) => transformOffer(offer)))
}
