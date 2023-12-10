import { apiAddress } from '.'

export const addUser = async (
    name,
    surname,
    age,
    adressId,
    phoneNr,
    rating
) => {
    return await fetch(`${apiAddress}/users`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            name,
            surname,
            age,
            address_id: adressId,
            phone_nr: phoneNr,
            rating,
        }),
    }).then((res) => res.json())
}
