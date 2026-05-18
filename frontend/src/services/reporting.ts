import api from './api'
import type { ReportRequest, ReportRequestCreate, ReportTemplate } from '@/types'

export const reportingService = {
  async getTemplates() {
    const { data } = await api.get<ReportTemplate[]>('/reports/templates')
    return data
  },
  async generateReport(request: ReportRequestCreate) {
    const { data } = await api.post<ReportRequest>('/reports/generate', request)
    return data
  },
  async getExportHistory() {
    const { data } = await api.get<ReportRequest[]>('/reports/export-history')
    return data
  },
  async getReportStatus(id: string) {
    const { data } = await api.get<ReportRequest>(`/reports/${id}`)
    return data
  }
}
