import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/home',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/catalogue',
      name: 'catalogue',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/CatalogueView.vue'),
    },
    {
    path: '/comics/:id',
    name: 'comics',
    component: () => import('../views/ComicsView.vue'),
    props: true
},
{
  path: '/auth',
  name: 'auth',
  component: () => import('../views/AuthView.vue'),
}
  ],
})

export default router
