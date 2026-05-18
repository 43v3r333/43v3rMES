import api from './api'
import type { DowntimeEvent, DowntimeEventCreate, DowntimeEventUpdate } from '@/types'

export const downtimeService = {
  async getEvents(params?: any) {
    const { data } = await api.get<DowntimeEvent[]>('/downtime-events/', { params })
    return data
  },
  async getEvent(id: string) {
    const { data } = await api.get<DowntimeEvent>(`/downtime-events/${id}`)
    return data
  },
  async createEvent(event: DowntimeEventCreate) {
    const { data } = await api.post<DowntimeEvent>('/downtime-events/', event)
    return data
  },
  async updateEvent(id: string, event: DowntimeEventUpdate) {
    const { data } = await api.patch<DowntimeEvent>(`/downtime-events/${id}`, event)
    return data
  }
}
