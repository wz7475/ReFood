import { apiAddress } from '.'

export const readUsers = async () => {
    return await fetch(`${apiAddress}/users`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then((res) => res.json())
        .then((res) =>
            res.map(
                ({ id, name, surname, age, address_id, phone_nr, rating }) => ({
                    id,

                    name,
                    surname,
                    age,
                    addressId: address_id,
                    phoneNr: phone_nr,
                    rating,
                })
            )
        )
}
