import { useMainStore } from "src/stores/mainStore"
import { useBackendStorage } from "./backendStorage"

export function useBackendApi() {
    const BackendUrl = process.env.BACKEND_URL || 'http://localhost:8000'

    function getAuth() {
        return useBackendStorage().getAuthorization()
    }

    function getHeaders(auth) {
        const headers = {
            accept: 'application/json',
            'Content-Type': 'application/json'
        }
        if (!!auth) {
            headers['Authorization'] = `Bearer ${auth}`
        }
        return headers
    }

    async function apiGet(url, auth) {
        url = `${BackendUrl}/${url}`
        console.debug('apiGet', url)
        const response = await fetch(url, {
            method: 'GET',
            mode: 'cors',
            headers: getHeaders(auth)
        })
        return await response.json()
    }

    async function apiPost(url, auth, body) {
        url = `${BackendUrl}/${url}`
        console.debug('apiPost', { url, body })
        const response = await fetch(url, {
            method: 'POST',
            headers: getHeaders(auth),
            body: JSON.stringify(body)
        })
        const jsonResponse = await response.json()
        console.debug('apiPost', { url, body, jsonResponse })
        return jsonResponse
    }

    const getLogin = async (username, password) => {
        return await apiPost('api/login', null, { username, password })
    }

    const getBackendVersion = async () => {
        try {
            const version = await apiGet('api/version')
            console.debug('api.getBackendVersion', version)
            return version.version
        }
        catch (err) {
            console.error('api.getBackendVersion', err)
        }
        return null
    }

    const getWhoAmI = async () => {
        try {
            const store = useMainStore()
            const whoami = await apiGet('api/whoami', store.auth.authorization)
            return whoami
        } catch (err) {
            console.error('api.getWhoAmI', err)
        }
    }

    const getAllPOS = async () => {
        try {
            const store = useMainStore()
            const allPos = await apiGet('api/pos', store.auth.authorization)
            return allPos
        } catch (err) {
            console.error('api.getAllPOS', err)
        }
    }


    return { apiGet, apiPost, getBackendVersion, getLogin, getWhoAmI, getAllPOS, getAuth }
}
