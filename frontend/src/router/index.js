import { route } from 'quasar/wrappers'
import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import routes from './routes'
import { useMainStore } from 'src/stores/mainStore'

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default route(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

  const store = useMainStore()


  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.VUE_ROUTER_BASE)
  })

  const publicPages = ['login']

  Router.beforeEach((to) => {
    const store = useMainStore()

    const authRequired = !publicPages.includes(to.name)

    if (authRequired && !store.isAuthorized) {
      store.returnUrl = to.fullPath
      console.debug('router.beforeEach: routing to login')
      return { name: 'login' }
    }
    if (store.isAuthorized && !authRequired) {
      console.debug(`router.beforeEach: routing to ${store.returnUrl || '/'}`)
      if (store.returnUrl)
        return { path: store.returnUrl }
      return { name: 'index' }
    }

  })

  return Router
})
