
const routes = [
  {
    path: '/auth',
    component: () => import('layouts/NoMenuLayout.vue'),
    children: [
      {
        path: 'login', component: () => import('pages/LoginPage.vue'),
        name: 'login'
      }
    ]
  },
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '', component: () => import('pages/IndexPage.vue'),
        name: 'index'
      }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
