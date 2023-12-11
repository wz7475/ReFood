import { apiAddress } from '.'

export const deleteAddress = async (addressId) => {
    return await fetch(`${apiAddress}/addresses/${addressId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then((res) => res.json())
}
