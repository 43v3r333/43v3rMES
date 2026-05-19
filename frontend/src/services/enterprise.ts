import api from './api'
import type { EnterpriseOverview, SiteComparisonItem } from '@/types'

export const enterpriseService = {
  async getOverview() {
    const { data } = await api.get<EnterpriseOverview>('/enterprise/overview')
    return data
  },
  async getSiteComparisons() {
    const { data } = await api.get<SiteComparisonItem[]>('/enterprise/site-comparison')
    return data
  }
}
