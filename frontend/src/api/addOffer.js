import { apiFetch } from '.'

export const addOffer = async (
    latitude,
    longitude,
    dishName,
    description,
    price,
    tags
) => {
    return await apiFetch('offers/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            latitude,
            longitude,
            dish_name: dishName,
            description,
            price,
            how_many_days_before_expiration: 0,
            tags,
        }),
    })
}
