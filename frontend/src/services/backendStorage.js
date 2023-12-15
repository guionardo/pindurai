import { LocalStorage } from "quasar"

const STORAGE_AUTH = 'pinturai_auth'

export const useBackendStorage = () => {
    /* Obtém a string de autorização para usar no header das requests */
    const getAuthorization = () => {
        const auth = getAuth()
        if (auth.authorization && validUntil > new Date()) {
            return auth.authorization
        }
        return null
    }

    /* Define a autorização e sua validade */
    const setAuth = (auth, validUntil) => {
        LocalStorage.set(STORAGE_AUTH, { authorization: auth, validUntil: validUntil })
    }

    const getAuth = () => {
        const auth = LocalStorage.getItem(STORAGE_AUTH) || {}
        auth.authorization = auth.authorization || null
        auth.validUntil = new Date(auth.validUntil || 0)
        return auth
    }

    const clear = () => {
        LocalStorage.remove(STORAGE_AUTH)
    }

    return { getAuthorization, setAuth, getAuth, clear }
}
