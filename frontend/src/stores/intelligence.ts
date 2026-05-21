import { defineStore } from 'pinia'
import { ref } from 'vue'
import { intelligenceService } from '@/services/intelligence'
import type { AIShiftSummary, OperationalRecommendation } from '@/types'

export const useIntelligenceStore = defineStore('intelligence', () => {
  const latestSummary = ref<AIShiftSummary | null>(null)
  const recommendations = ref<OperationalRecommendation[]>([])
  const isLoading = ref(false)

  async function fetchIntelligence() {
    isLoading.value = true
    try {
      const [summary, recs] = await Promise.all([
        intelligenceService.getShiftSummary(),
        intelligenceService.getRecommendations()
      ])
      latestSummary.value = summary
      recommendations.value = recs
    } finally {
      isLoading.value = false
    }
  }

  return { latestSummary, recommendations, isLoading, fetchIntelligence }
})
