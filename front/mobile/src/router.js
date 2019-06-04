import Vue from 'vue'
import Router from 'vue-router'
import Index from './views/Index.vue'

Vue.use(Router)

export default new Router({
  routes: [{
      path: '/',
      alias: '/index',
      name: 'index',
      component: Index,
      children: [{
        path: 'indexcate',
        name: 'indexcate',
        component: () => import( /* webpackChunkName: "indexcate" */ './views/index/IndexCate.vue')
      }, {
        path: 'indexlast',
        name: 'indexlast',
        component: () => import( /* webpackChunkName: "indexlast" */ './views/index/IndexLast.vue')
      }]
    },
    {
      path: '/search',
      name: 'search',
      component: () => import( /* webpackChunkName: "search" */ './views/index/Search.vue')
    },
    {
      path: '/read',
      name: 'read',
      component: () => import( /* webpackChunkName: "read" */ './views/index/Read.vue')
    },
    {
      path: '/catelist',
      name: 'catelist',
      component: () => import( /* webpackChunkName: "catelist" */ './views/index/CateList.vue')
    },
    {
      path: '/auth',
      name: 'auth',
      redirect: '/auth/login',
      component: () => import( /* webpackChunkName: "auth" */ './views/Auth.vue'),
      children: [{
          path: 'login',
          name: 'login',
          component: () => import( /* webpackChunkName: "login" */ './views/auth/Login.vue'),
        },
        {
          path: 'register',
          name: 'register',
          component: () => import( /* webpackChunkName: "register" */ './views/auth/Register.vue'),
        }
      ]
    }
  ]
})