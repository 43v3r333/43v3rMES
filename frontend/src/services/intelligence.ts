import api from './api'
import type { AIShiftSummary, OperationalRecommendation, RiskAnalysis } from '@/types'

export const intelligenceService = {
  async getShiftSummary() {
    const { data } = await api.get<AIShiftSummary>('/intelligence/shift-summaries')
    return data
  },
  async getRecommendations() {
    const { data } = await api.get<OperationalRecommendation[]>('/intelligence/recommendations')
    return data
  },
  async getRiskAnalysis(machineId: string) {
    const { data } = await api.get<RiskAnalysis>(`/intelligence/risk-analysis/${machineId}`)
    return data
  }
}
