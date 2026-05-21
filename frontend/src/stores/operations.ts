import { defineStore } from 'pinia'
import { ref } from 'vue'
import { operationsService } from '@/services/operations'
import type { OperationsOverview, ActiveIncident, MachineStatus } from '@/types'

export const useOperationsStore = defineStore('operations', () => {
  const overview = ref<OperationsOverview | null>(null)
  const activeIncidents = ref<ActiveIncident[]>([])
  const machineStatus = ref<MachineStatus[]>([])
  const isLoading = ref(false)

  async function fetchAll() {
    isLoading.value = true
    try {
      const [ov, incidents, machines] = await Promise.all([
        operationsService.getOverview(),
        operationsService.getActiveIncidents(),
        operationsService.getMachineStatus()
      ])
      overview.value = ov
      activeIncidents.value = incidents
      machineStatus.value = machines
    } finally {
      isLoading.value = false
    }
  }

  return { overview, activeIncidents, machineStatus, isLoading, fetchAll }
})
