import { defineStore } from 'pinia'
import { ref } from 'vue'
import { enterpriseService } from '@/services/enterprise'
import type { EnterpriseOverview, SiteComparisonItem } from '@/types'

export const useEnterpriseStore = defineStore('enterprise', () => {
  const overview = ref<EnterpriseOverview | null>(null)
  const siteComparisons = ref<SiteComparisonItem[]>([])
  const isLoading = ref(false)

  async function fetchEnterpriseData() {
    isLoading.value = true
    try {
      const [ov, comps] = await Promise.all([
        enterpriseService.getOverview(),
        enterpriseService.getSiteComparisons()
      ])
      overview.value = ov
      siteComparisons.value = comps
    } finally {
      isLoading.value = false
    }
  }

  return { overview, siteComparisons, isLoading, fetchEnterpriseData }
})
