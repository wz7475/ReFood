import { apiFetch } from '.'

export const offerDetails = async (id) => {
    const offerStateLookup = ['open', 'reserved', 'complete']
    const dishTagLookup = ['vege', 'spicy', 'glutenFree', 'sugarFree']

    return await apiFetch(`offers/${id}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(
        ({
            buyer_name,
            buyer_surname,
            dish_description,
            dish_name,
            latitude,
            longitude,
            offer_id,
            offer_state,
            price,
            seller_name,
            seller_surname,
            tags,
        }) => ({
            id: offer_id,
            distance: 0.5,
            price,
            dishName: dish_name,
            sellerName: `${seller_name} ${seller_surname}`,
            buyerName: `${buyer_name} ${buyer_surname}`,
            tags: tags.map((val) => dishTagLookup[val]),
            description: dish_description,
            latitude,
            longitude,
            offerState: offerStateLookup[offer_state],
        })
    )
}
