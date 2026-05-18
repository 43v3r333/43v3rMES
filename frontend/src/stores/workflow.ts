import { defineStore } from 'pinia'
import { ref } from 'vue'
import { workflowService } from '@/services/workflow'
import type { Shift, ShiftHandover } from '@/types'

export const useWorkflowStore = defineStore('workflow', () => {
  const shifts = ref<Shift[]>([])
  const handovers = ref<ShiftHandover[]>([])
  const currentHandover = ref<ShiftHandover | null>(null)
  const isLoading = ref(false)

  async function fetchShifts() {
    isLoading.value = true
    try {
      shifts.value = await workflowService.getShifts()
    } finally {
      isLoading.value = false
    }
  }

  async function fetchHandovers() {
    isLoading.value = true
    try {
      handovers.value = await workflowService.getHandovers()
    } finally {
      isLoading.value = false
    }
  }

  async function fetchHandover(id: string) {
    isLoading.value = true
    try {
      currentHandover.value = await workflowService.getHandover(id)
    } finally {
      isLoading.value = false
    }
  }

  return { shifts, handovers, currentHandover, isLoading, fetchShifts, fetchHandovers, fetchHandover }
})
