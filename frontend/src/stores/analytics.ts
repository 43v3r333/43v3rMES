import { defineStore } from 'pinia'
import { ref } from 'vue'
import { analyticsService } from '@/services/analytics'
import type { KPIResponse, ParetoItem, AgingIssue } from '@/types'

export const useAnalyticsStore = defineStore('analytics', () => {
  const kpis = ref<KPIResponse | null>(null)
  const paretoData = ref<ParetoItem[]>([])
  const openIssues = ref<AgingIssue[]>([])
  const isLoading = ref(false)

  async function fetchKPIs(filters?: any) {
    isLoading.value = true
    try {
      kpis.value = await analyticsService.getKPIs(filters)
    } finally {
      isLoading.value = false
    }
  }

  async function fetchPareto(filters?: any) {
    isLoading.value = true
    try {
      paretoData.value = await analyticsService.getPareto(filters)
    } finally {
      isLoading.value = false
    }
  }

  return { kpis, paretoData, openIssues, isLoading, fetchKPIs, fetchPareto }
})
