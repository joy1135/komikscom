import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useAuthStore } from '@/stores/auth'

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
}    ,{
      path: '/favourite',
      name: 'favourite',
      component: () => import('../views/FavView.vue'),
    },
    {
  path: '/comic/:comic_id/chapter/:chapter_id/page/:page_number',
  name: 'reader',
  component: () => import('@/views/ReadView.vue'),
  props: true
},
{
    path: '/your_profile',
    name: 'profile',
    component: () => import('@/views/ProfileView.vue'),
  },
  {
    path: '/create-comic',
    name: 'create-comic',
    component: () => import('@/views/CreaterView.vue'),
    meta: {requiresCreator: true }
  }
  
  ]
  
})
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  // Проверка прав на создание комиксов
  if (to.meta.requiresCreator) {
    const canCreate = authStore.role === 1 || authStore.role === 3
    if (!canCreate) {
      next('/') // Или на страницу с ошибкой доступа
      return
    }
  }
  
  next()
})
export default router
