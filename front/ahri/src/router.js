import Vue from 'vue'
import Router from 'vue-router'
import Index from './views/Index.vue'

import store from './store'

Vue.use(Router)

const router = new Router({
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
        },
        {
          path: 'forget',
          name: 'forget',
          component: () => import( /* webpackChunkName: "forget" */ './views/auth/Forget.vue'),
        }
      ]
    },
    {
      path: '/admin',
      name: 'admin',
      meta: {
        required: true
      },
      component: () => import( /* webpackChunkName: "admin" */ './views/Admin.vue'),
      redirect: '/admin/welcome',
      children: [{
          path: 'welcome',
          name: 'welcome',
          meta: {
            required: true
          },
          component: () => import( /* webpackChunkName: "welcome" */ './views/admin/Welcome.vue'),
        },
        {
          path: 'sysinfo',
          name: 'sysinfo',
          meta: {
            required: true
          },
          component: () => import( /* webpackChunkName: "sysinfo" */ './views/admin/SysInfo.vue'),
          children: [{
            path: 'bg',
            name: 'bg',
            component: () => import( /* webpackChunkName: "setting_bg" */ './views/admin/setting/Bg.vue'),
          }, ]
        },
        {
          path: 'category',
          name: 'category',
          meta: {
            required: true
          },
          component: () => import( /* webpackChunkName: "category" */ './views/admin/Category.vue'),
        },
        {
          path: 'article',
          name: 'article',
          meta: {
            required: true
          },
          component: () => import( /* webpackChunkName: "article" */ './views/admin/Article.vue'),
        },
        {
          path: 'newart',
          name: 'newart',
          meta: {
            required: true
          },
          component: () => import( /* webpackChunkName: "newart" */ './views/admin/NewArticle.vue'),
        },
        {
          path: 'comment',
          name: 'comment',
          meta: {
            required: true
          },
          component: () => import( /* webpackChunkName: "comment" */ './views/admin/Comment.vue')
        },
        {
          path: 'myinfo',
          name: 'myinfo',
          meta: {
            required: true
          },
          component: () => import( /* webpackChunkName: "myinfo" */ './views/admin/MyInfo.vue')
        },
        {
          path: 'user',
          name: 'user',
          meta: {
            required: true
          },
          component: () => import( /* webpackChunkName: "user" */ './views/admin/UserManage.vue')
        },
      ]
    }
  ]
})

router.beforeEach((to, from, next) => {
  let is_login = store.state.user || false;
  if (to.meta.required) {
    if (is_login && store.state.user.role >= 10) {
      next();
    } else {
      next('/auth/login');
    }
  } else {
    next();
  }
})

export default router;