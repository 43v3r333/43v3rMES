import { createRouter, createWebHistory } from 'vue-router'; import { useAuthStore } from '@/stores/auth'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', name: 'login', component: () => import('@/views/LoginView.vue') },
    { path: '/', component: () => import('@/layouts/DashboardLayout.vue'), children: [{ path: '', name: 'dashboard', component: () => import('@/views/DashboardView.vue') }] }
  ]
})
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore(); if (to.name !== 'login' && !authStore.isAuthenticated) next({ name: 'login' }); else next()
})
export default router
