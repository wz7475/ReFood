import { apiAddress } from '.'

export const deleteOffer = async (offerId) => {
    return await fetch(`${apiAddress}/offers/${offerId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then((res) => res.json())
}
