import { defineStore } from 'pinia'
import { ref } from 'vue'
import { factoryService } from '@/services/factory'
import type { Factory, Machine } from '@/types'

export const useFactoryStore = defineStore('factory', () => {
  const factories = ref<Factory[]>([])
  const machines = ref<Machine[]>([])
  const isLoading = ref(false)

  async function fetchFactories() {
    isLoading.value = true
    try {
      factories.value = await factoryService.getFactories()
    } finally {
      isLoading.value = false
    }
  }

  async function fetchMachines() {
    isLoading.value = true
    try {
      machines.value = await factoryService.getMachines()
    } finally {
      isLoading.value = false
    }
  }

  return { factories, machines, isLoading, fetchFactories, fetchMachines }
})
