<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useFactoryStore } from '@/stores/factory'
import BaseTable from '@/components/ui/BaseTable.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { Plus, Search, Filter } from 'lucide-vue-next'

const factoryStore = useFactoryStore()

const columns = [
  { key: 'name', label: 'Machine Name' },
  { key: 'code', label: 'Serial/Asset Code' },
  { key: 'line_id', label: 'Production Line' },
  { key: 'created_at', label: 'Commission Date' },
]

onMounted(() => {
  factoryStore.fetchMachines()
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Machine Assets</h1>
        <p class="text-sm text-muted-foreground">Manage and monitor manufacturing equipment across all lines.</p>
      </div>
      <div class="flex items-center space-x-2">
        <BaseButton variant="outline" class="h-9 px-3">
          <Filter class="mr-2 h-4 w-4" />
          Filter
        </BaseButton>
        <BaseButton variant="primary" class="h-9 px-3">
          <Plus class="mr-2 h-4 w-4" />
          Register Machine
        </BaseButton>
      </div>
    </div>

    <div class="bg-card border rounded-lg shadow-sm">
      <div class="p-4 border-b flex items-center justify-between bg-muted/20">
        <div class="relative w-full max-w-sm">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search by code or name..."
            class="w-full pl-9 pr-4 py-2 bg-background border rounded-md text-sm focus:ring-1 focus:ring-primary outline-none"
          />
        </div>
        <div class="text-xs text-muted-foreground font-medium uppercase tracking-tighter">
          Total: {{ factoryStore.machines.length }} Assets
        </div>
      </div>

      <BaseTable :columns="columns" :data="factoryStore.machines">
        <template #cell(line_id)="{ row }">
          <span class="text-xs font-mono text-muted-foreground">{{ row.line_id.split('-')[0] }}...</span>
        </template>
        <template #cell(created_at)="{ row }">
          {{ new Date(row.created_at).toLocaleDateString() }}
        </template>
        <template #empty>
          <div class="py-12 text-center text-muted-foreground">
            No machines registered in this tenant yet.
          </div>
        </template>
      </BaseTable>
    </div>
  </div>
</template>
