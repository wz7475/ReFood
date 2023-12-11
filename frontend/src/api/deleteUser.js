import { apiAddress } from '.'

export const deleteUser = async (userId) => {
    return await fetch(`${apiAddress}/users/${userId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then((res) => res.json())
}
