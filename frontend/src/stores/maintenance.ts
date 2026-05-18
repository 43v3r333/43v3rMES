import { defineStore } from 'pinia'
import { ref } from 'vue'
import { maintenanceService } from '@/services/maintenance'
import type { WorkOrder, PMSchedule } from '@/types'

export const useMaintenanceStore = defineStore('maintenance', () => {
  const workOrders = ref<WorkOrder[]>([])
  const pmSchedules = ref<PMSchedule[]>([])
  const isLoading = ref(false)

  async function fetchWorkOrders(filters?: any) {
    isLoading.value = true
    try {
      workOrders.value = await maintenanceService.getWorkOrders(filters)
    } finally {
      isLoading.value = false
    }
  }

  async function fetchPMSchedules() {
    isLoading.value = true
    try {
      pmSchedules.value = await maintenanceService.getPMSchedules()
    } finally {
      isLoading.value = false
    }
  }

  return { workOrders, pmSchedules, isLoading, fetchWorkOrders, fetchPMSchedules }
})
