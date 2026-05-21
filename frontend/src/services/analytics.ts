import api from './api'
import type { KPIResponse, ParetoItem, AgingIssue } from '@/types'

export const analyticsService = {
  async getKPIs(params?: any) {
    const { data } = await api.get<KPIResponse>('/analytics/kpis', { params })
    return data
  },
  async getPareto(params?: any) {
    const { data } = await api.get<ParetoItem[]>('/analytics/pareto', { params })
    return data
  },
  async getOpenIssues() {
    const { data } = await api.get<AgingIssue[]>('/analytics/open-issues')
    return data
  }
}
