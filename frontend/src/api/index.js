import { useAppStore } from '@/store/app'
//export const apiAddress = 'http://maluch.mikr.us:40481'
export const apiAddress = '/api'

export const apiFetch = async (endpoint, options) => {
    const appStore = useAppStore()
    return await fetch(`${apiAddress}/${endpoint}`, options)
        .then((res) => {
            if (res.status === 403) {
                appStore.logout()
                throw new Error('session expired')
            }
            if (res.ok) return res.json()
            return Promise.reject(res)
        })
        .then((res) => {
            console.log(res)
            return res
        })
}

export * from './login'
export * from './register'
export * from './myOffers'
export * from './searchOffers'
export * from './addOffer'
export * from './offerDetails'
export * from './completeOffer'
export * from './reserveOffer'
