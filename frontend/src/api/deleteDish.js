import { apiAddress } from '.'

export const deleteDish = async (dishId) => {
    return await fetch(`${apiAddress}/dishes/${dishId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then((res) => res.json())
}
