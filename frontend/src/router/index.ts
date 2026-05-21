import { createRouter, createWebHistory } from 'vue-router'; import { useAuthStore } from '@/stores/auth'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/:pathMatch(.*)*', name: 'not-found', component: () => import('@/pages/NotFoundPage.vue') },
    { path: '/login', name: 'login', component: () => import('@/pages/LoginView.vue') },
    {
      path: '/',
      component: () => import('@/layouts/DashboardLayout.vue'),
      children: [
        { path: '', name: 'dashboard', component: () => import('@/pages/OperationsCommandCenterPage.vue') },
        { path: 'diagnostics', name: 'diagnostics', component: () => import('@/pages/DiagnosticsPage.vue') },
        { path: 'enterprise', name: 'enterprise', component: () => import('@/pages/EnterpriseOverviewPage.vue') },
        { path: 'intelligence', name: 'intelligence', component: () => import('@/pages/IntelligencePage.vue') },
        { path: 'reports', name: 'reports', component: () => import('@/pages/ReportingPage.vue') },
        { path: 'maintenance/schedules', name: 'pm-schedules', component: () => import('@/pages/PMSchedulesPage.vue') },
        { path: 'maintenance', name: 'maintenance', component: () => import('@/pages/WorkOrderPage.vue') },
        { path: 'escalations', name: 'escalations', component: () => import('@/pages/EscalationsPage.vue') },
        { path: 'analytics', name: 'analytics', component: () => import('@/pages/AnalyticsPage.vue') },
        { path: 'handovers', name: 'handovers', component: () => import('@/pages/ShiftHandoverPage.vue') },
        { path: 'downtime', name: 'downtime', component: () => import('@/pages/DowntimePage.vue') },
        { path: 'factories', name: 'factories', component: () => import('@/pages/FactoriesPage.vue') },
        { path: 'machines', name: 'machines', component: () => import('@/pages/MachinesPage.vue') }
      ]
    }
  ]
})
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  if (!authStore.hasTriedRestore) {
    await authStore.restoreSession()
  }
  if (to.name !== 'login' && !authStore.isAuthenticated) {
    next({ name: 'login' })
  } else {
    next()
  }
})
export default router
