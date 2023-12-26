import { apiFetch } from '.'

export const login = async (login, password) => {
    return await apiFetch('login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            login,
            password,
        }),
    })
}
