const offerStateLookup = ['open', 'reserved', 'complete']
const dishTagLookup = ['vege', 'spicy', 'glutenFree', 'sugarFree']

export const transformOffer = (offer) => {
    const {
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
    } = offer

    return {
        id: offer_id,
        distance: 0.5,
        price,
        dishName: dish_name,
        sellerName: seller_name ? `${seller_name} ${seller_surname}` : null,
        buyerName: buyer_name ? `${buyer_name} ${buyer_surname}` : null,
        tags: tags.map((val) => dishTagLookup[val]),
        description: dish_description,
        latitude,
        longitude,
        state: offerStateLookup[offer_state],
    }
}
