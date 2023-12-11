import { apiAddress } from '.'

export const addOffer = async (dishId, sellerId, addressId) => {
    return await fetch(`${apiAddress}/offers`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            dish_id: dishId,
            seller_id: sellerId,
            address_id: addressId,
        }),
    }).then((res) => res.json())
}
