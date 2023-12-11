import { apiAddress } from '.'

export const readOffers = async () => {
    return await fetch(`${apiAddress}/offers`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then((res) => res.json())
        .then((res) =>
            res.map(({ id, dish_id, seller_id, address_id }) => ({
                id,

                dishId: dish_id,
                sellerId: seller_id,
                addressId: address_id,
            }))
        )
}
