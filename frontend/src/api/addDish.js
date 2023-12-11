import { apiAddress } from '.'

export const addDish = async (
    name,
    isVegetarian,
    description,
    price,
    howManyDaysBeforeExpiration
) => {
    return await fetch(`${apiAddress}/dishes`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            name,
            is_vegetarian: isVegetarian,
            description,
            price,
            how_many_days_before_expiration: howManyDaysBeforeExpiration,
        }),
    }).then((res) => res.json())
}
