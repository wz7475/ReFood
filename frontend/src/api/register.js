import { apiFetch, login } from '.'

export const register = async (
    name,
    surname,
    loginVal,
    password,
    phoneNumber
) => {
    await apiFetch('register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({
            name,
            surname,
            login: loginVal,
            password,
            phone_nr: phoneNumber,
        }),
    })

    await login(loginVal, password)
}
