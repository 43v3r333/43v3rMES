import api from './api'
import type { Shift, ShiftCreate, ShiftHandover, ShiftHandoverCreate } from '@/types'

export const workflowService = {
  async getShifts() {
    const { data } = await api.get<Shift[]>('/shifts')
    return data
  },
  async createShift(shift: ShiftCreate) {
    const { data } = await api.post<Shift>('/shifts', shift)
    return data
  },
  async getHandovers() {
    const { data } = await api.get<ShiftHandover[]>('/shift-handovers')
    return data
  },
  async getHandover(id: string) {
    const { data } = await api.get<ShiftHandover>(`/shift-handovers/${id}`)
    return data
  },
  async createHandover(handover: ShiftHandoverCreate) {
    const { data } = await api.post<ShiftHandover>('/shift-handovers', handover)
    return data
  }
}
