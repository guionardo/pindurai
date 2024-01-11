
const routes = [
  {
    path: '/',
    component: () => import('layouts/NoMenuLayout.vue'),
    children: [
      {
        path: '',
        component: () => import('pages/IndexPage.vue'),
        name: 'index'
      }, {
        path: 'login', component: () => import('pages/LoginPage.vue'),
        name: 'login'
      }
    ]
  },
  {
    path: '/pdv',
    component: () => import('layouts/MainLayout.vue'),

    children: [
      {
        path: ':pdv_id',
        component: () => import('pages/HomePage.vue'),
        name: 'home',
        props: true,
      },
      {
        path: '',
        component: () => import('pages/HomePage.vue'),
        name: 'home_default',
      }
    ]
  },


  {
    path: '/no_backend/:returnUrl',
    name: 'no_backend',
    component: () => import('pages/ErrBackendOffline.vue')
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
