import api from './api'
import type { WorkOrder, WorkOrderCreate, WorkOrderUpdate, PMSchedule } from '@/types'

export const maintenanceService = {
  async getWorkOrders(params?: any) {
    const { data } = await api.get<WorkOrder[]>('/work-orders', { params })
    return data
  },
  async createWorkOrder(wo: WorkOrderCreate) {
    const { data } = await api.post<WorkOrder>('/work-orders', wo)
    return data
  },
  async updateWorkOrder(id: string, wo: WorkOrderUpdate) {
    const { data } = await api.patch<WorkOrder>(`/work-orders/${id}`, wo)
    return data
  },
  async getPMSchedules() {
    const { data } = await api.get<PMSchedule[]>('/preventive-maintenance')
    return data
  }
}
