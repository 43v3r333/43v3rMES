import api from './api'
import type { OperationsOverview, ActiveIncident, MachineStatus } from '@/types'

export const operationsService = {
  async getOverview() {
    const { data } = await api.get<OperationsOverview>('/operations/overview')
    return data
  },
  async getActiveIncidents() {
    const { data } = await api.get<ActiveIncident[]>('/operations/active-incidents')
    return data
  },
  async getMachineStatus() {
    const { data } = await api.get<MachineStatus[]>('/operations/machine-status')
    return data
  }
}
