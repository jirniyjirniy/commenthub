import { createApp, provide, h } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import { DefaultApolloClient } from '@vue/apollo-composable'
import { apolloClient } from './api/apollo'
import './index.css'
import App from './App.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import Home from './views/Home.vue'
import GraphqlDemo from './views/GraphqlDemo.vue'

const pinia = createPinia()

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/comments/:id',
      name: 'comment-detail',
      component: () => import('./views/CommentDetail.vue')
    },
    {
      path: '/graphql',
      name: 'graphql',
      component: GraphqlDemo
    }
  ],
})

const app = createApp({
  setup() {
    provide(DefaultApolloClient, apolloClient)
  },
  render: () => h(App),
})

app.use(pinia)
app.use(router)
app.mount('#app')