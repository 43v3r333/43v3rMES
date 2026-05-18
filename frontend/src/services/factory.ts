import api from './api'
import type { Factory, FactoryCreate, Machine, MachineCreate } from '@/types'

export const factoryService = {
  async getFactories() {
    const { data } = await api.get<Factory[]>('/factories/')
    return data
  },
  async createFactory(factory: FactoryCreate) {
    const { data } = await api.post<Factory>('/factories/', factory)
    return data
  },
  async getMachines() {
    const { data } = await api.get<Machine[]>('/machines/')
    return data
  },
  async createMachine(machine: MachineCreate) {
    const { data } = await api.post<Machine>('/machines/', machine)
    return data
  }
}
