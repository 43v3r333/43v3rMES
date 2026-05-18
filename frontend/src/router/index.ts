import { createRouter, createWebHistory } from 'vue-router'; import { useAuthStore } from '@/stores/auth'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('@/pages/NotFoundPage.vue') },
    { path: '/login', name: 'login', component: () => import('@/pages/LoginView.vue') },
    { path: '/', component: () => import('@/layouts/DashboardLayout.vue'), children: [{ path: '', name: 'dashboard', component: () => import('@/pages/DashboardPage.vue') }] }
        { path: 'handovers', name: 'handovers', component: () => import('@/pages/ShiftHandoverPage.vue') },
        { path: 'downtime', name: 'downtime', component: () => import('@/pages/DowntimePage.vue') },
        { path: 'factories', name: 'factories', component: () => import('@/pages/FactoriesPage.vue') },
        { path: 'machines', name: 'machines', component: () => import('@/pages/MachinesPage.vue') },
  ]
})
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore(); if (to.name !== 'login' && !authStore.isAuthenticated) next({ name: 'login' }); else next()
})
export default router
