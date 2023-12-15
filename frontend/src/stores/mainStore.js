import { defineStore } from 'pinia'
import { LocalStorage } from 'quasar'
import { useBackendApi } from 'src/services/backendApi'
import { useBackendStorage } from 'src/services/backendStorage'
import { useRouter } from 'vue-router'

const USER = 'pindurai_user'
const STORAGE_AUTH = 'pinturai_auth'

const api = useBackendApi()
const storage = useBackendStorage()
const router = useRouter()


export const useMainStore = defineStore('main', {

  state: () => ({
    auth: storage.getAuth(),
    backend: {
      version: null,
      lastFetch: new Date(0)
    },
    returnUrl: null,
    username: storage.getUser(),
    pos: []
  }),

  getters: {
    backendHealth(state) {
      return (state.backend.version && (new Date().getTime() - state.backend.lastFetch.getTime()) < 60000)
    },
    isAuthorized(state) {
      return state.auth.authorization && state.auth.validUntil > new Date()
    }
  },

  actions: {
    async login(username, password) {
      try {
        const auth = await api.getLogin(username, password)
        console.debug(`AUTH: login(${username},${password}) -> ${auth}`)
        this.auth.authorization = auth.token
        this.auth.validUntil = new Date(auth.valid_until)
        storage.setAuth(this.auth.authorization, this.auth.validUntil)
        // await useRouter().push(this.returnUrl || '/')
        console.info(`AUTH: login(${username}) -> ${this.authorization} until ${this.validUntil}`)
        return this.auth
      } catch (err) {
        console.error(`AUTH: login(${username})`, err)
        this.logout()
      }
    },
    logout() {
      this.authorization = null
      this.validUntil = new Date(0)
      storage.clear()
      useRouter.push({ name: 'login' })
    },
    setBackendVersion(version) {
      this.backend = { version: version.version, lastFetch: new Date() }
    },
    async updateBackendStatus() {
      let version = 'UNAVALIABLE'
      try {
        version = await api.getBackendVersion()
      } catch (err) {
        console.error('BACKEND STATUS', err)
      }
      this.backend.version = version
      this.backend.lastFetch = new Date()
    },
    async getWhoIAm() {
      try {
        const user = await api.getWhoAmI()
        this.username = user

      } catch (err) {
        console.error('AUTH: getWhoIAm', err)
      }
    },

    async getAllPos() {
      try {
        const pos = await api.getAllPOS()
        console.debug('POS: getAllPos', pos)
        this.pos = pos

      } catch (err) {
        console.error('POS: getAllPos', err)
      }
    },
  }
})
