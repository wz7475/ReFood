import { apiAddress } from '.'

export const readDishes = async () => {
    return await fetch(`${apiAddress}/dishes`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then((res) => res.json())
        .then((res) =>
            res.map(
                ({
                    id,
                    name,
                    is_vegetarian,
                    description,
                    price,
                    how_many_days_before_expiration,
                }) => ({
                    id,

                    name,
                    isVegetarian: is_vegetarian,
                    description,
                    price,
                    howManyDaysBeforeExpiration:
                        how_many_days_before_expiration,
                })
            )
        )
}
