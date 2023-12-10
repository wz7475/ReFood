import { apiAddress } from '.'

export const readAddresses = async () => {
    return await fetch(`${apiAddress}/addresses`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then((res) => res.json())
}
