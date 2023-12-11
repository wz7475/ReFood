import { apiAddress } from '.'

export const readAddresses = async () => {
    return await fetch(`${apiAddress}/addresses`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then((res) => res.json())
        .then((res) =>
            res.map((address) => ({
                id: address.id,

                streetName: address.street_name,
                houseNr: address.house_nr,
                apartamentNr: address.apartament_nr,
                city: address.city,
            }))
        )
}
