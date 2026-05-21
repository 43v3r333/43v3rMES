import { defineStore } from 'pinia'
import { ref } from 'vue'
import { reportingService } from '@/services/reporting'
import type { ReportRequest, ReportTemplate } from '@/types'

export const useReportingStore = defineStore('reporting', () => {
  const templates = ref<ReportTemplate[]>([])
  const exportHistory = ref<ReportRequest[]>([])
  const isLoading = ref(false)

  async function fetchTemplates() {
    isLoading.value = true
    try {
      templates.value = await reportingService.getTemplates()
    } finally {
      isLoading.value = false
    }
  }

  async function fetchExportHistory() {
    isLoading.value = true
    try {
      exportHistory.value = await reportingService.getExportHistory()
    } finally {
      isLoading.value = false
    }
  }

  return { templates, exportHistory, isLoading, fetchTemplates, fetchExportHistory }
})
