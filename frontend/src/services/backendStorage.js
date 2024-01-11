const STORAGE = 'pindurai'

const serialize = (data) => JSON.stringify(data)
const deserialize = (json) => {
    const data = JSON.parse(json)
    for (const prop in data) {
        if (data.hasOwnProperty(prop)) {
            let value = data[prop]
            const d = new Date(data[prop])
            if (!isNaN(d)) {
                data[prop] = d
            } else {
                data[prop] = value
            }
        }
    }
    return data
}

export const useBackendStorage = () => {

    const getStorage = (key) => {
        key = `${STORAGE}_${key}`
        const value = deserialize(localStorage.getItem(key) || '{}')
        console.info(`backendStorage.getStorage(${key})`, value)
        return value
    }

    const setStorage = (key, value) => {
        key = `${STORAGE}_${key}`
        console.info(`backendStorage.setStorage(${key})`, value)
        localStorage.setItem(key, serialize(value))
    }


    /* Obtém a string de autorização para usar no header das requests */
    const getAuthorization = () => {
        // debugger // eslint-disable-line no-debugger
        const auth = getAuth()
        if (auth.authorization && auth.validUntil > new Date()) {
            return auth.authorization
        }
        return null
    }

    /* Define a autorização e sua validade */
    const setAuth = (auth, validUntil) => {
        setStorage('auth', { authorization: auth, validUntil: validUntil })
    }


    const getAuth = () => {
        const auth = getStorage('auth') || {}
        auth.authorization = auth.authorization || null
        auth.validUntil = new Date(auth.validUntil || 0)
        return auth
    }

    const getUser = () => getStorage('user') || {}
    const setUser = (user) => setStorage('user', user)

    const clear = () => {
        localStorage.remove(STORAGE)
    }

    return { getAuthorization, setAuth, getAuth, clear, getUser, setUser }
}
