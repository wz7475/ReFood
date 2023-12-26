import { apiFetch } from '.'

export const myOffers = async () => {
    return await apiFetch('my_offers', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
    })
}
