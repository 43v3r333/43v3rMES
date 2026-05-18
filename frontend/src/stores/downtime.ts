import { defineStore } from 'pinia'
import { ref } from 'vue'
import { downtimeService } from '@/services/downtime'
import type { DowntimeEvent } from '@/types'

export const useDowntimeStore = defineStore('downtime', () => {
  const events = ref<DowntimeEvent[]>([])
  const currentEvent = ref<DowntimeEvent | null>(null)
  const isLoading = ref(false)

  async function fetchEvents(filters?: any) {
    isLoading.value = true
    try {
      events.value = await downtimeService.getEvents(filters)
    } finally {
      isLoading.value = false
    }
  }

  async function fetchEvent(id: string) {
    isLoading.value = true
    try {
      currentEvent.value = await downtimeService.getEvent(id)
    } finally {
      isLoading.value = false
    }
  }

  return { events, currentEvent, isLoading, fetchEvents, fetchEvent }
})
