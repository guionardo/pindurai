import { defineStore } from 'pinia'
import { useBackendApi } from 'src/services/backendApi'
import { useBackendStorage } from 'src/services/backendStorage'
import { useRouter } from 'vue-router'
import { Dialog } from 'quasar'

const USER = 'pindurai_user'
const STORAGE_AUTH = 'pinturai_auth'

const api = useBackendApi()
const storage = useBackendStorage()

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
      console.group('LOGIN', { username, password })
      let response = {}
      const auth = await api.getLogin(username, password)
      if (!auth.token) {
        console.error('LOGIN FAILED')
        const dialog = Dialog.create({
          title: 'Atenção',
          message: 'Login não foi autorizado',
        }).onOk(() => console.warn('Login failed acknowledeged'))

      } else {
        this.auth.authorization = auth.token
        this.auth.validUntil = auth.valid_until
        storage.setAuth(auth.token, auth.valid_until)
        console.info(`USER ${username} LOGGED: Authorization ${auth.token} valid until ${auth.valid_until}`)
        response = {
          authorization: auth.token,
          validUNtil: auth.valid_until
        }
        await useRouter().push(this.returnUrl || '/')
      }
      // try {
      //   console.debug(`AUTH: login(${username},${password}) -> ${auth}`)
      //   this.auth.authorization = auth.token
      //   this.auth.validUntil = new Date(auth.valid_until)
      //   storage.setAuth(this.auth.authorization, this.auth.validUntil)
      //   // await useRouter().push(this.returnUrl || '/')
      //   console.info(`AUTH: login(${username}) -> ${this.authorization} until ${this.validUntil}`)
      //   const router = useRouter()
      //   router.push({ name: "index" })
      //   return this.auth
      // } catch (err) {
      //   console.error(`AUTH: login(${username})`, err)
      //   // this.logout()
      // }
      console.groupEnd()
      return response
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
        // debugger
        const pos = await api.getAllPOS()
        console.debug('POS: getAllPos', pos)
        this.pos = pos

      } catch (err) {
        console.error('POS: getAllPos', err)
      }
    },
  }
})
