<script setup lang="ts">
import { onMounted } from 'vue'
import { useMaintenanceStore } from '@/stores/maintenance'
import BaseTable from '@/components/ui/BaseTable.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { Calendar, Plus, ShieldCheck } from 'lucide-vue-next'

const maintenanceStore = useMaintenanceStore()

const columns = [
  { key: 'name', label: 'Schedule Name' },
  { key: 'machine_id', label: 'Asset' },
  { key: 'interval_days', label: 'Interval' },
  { key: 'next_due_at', label: 'Next Due' },
  { key: 'is_active', label: 'Status' },
]

onMounted(() => {
  maintenanceStore.fetchPMSchedules()
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Preventive Maintenance</h1>
        <p class="text-sm text-muted-foreground uppercase font-black tracking-tighter">Reliability & Asset Integrity Schedules</p>
      </div>
      <BaseButton variant="primary">
        <Plus class="mr-2 h-4 w-4" />
        Create PM Schedule
      </BaseButton>
    </div>

    <div class="bg-card border rounded-lg shadow-sm">
      <div class="p-4 border-b bg-muted/20 flex items-center justify-between">
        <div class="flex items-center">
          <Calendar class="mr-2 h-4 w-4 text-primary" />
          <h3 class="text-xs font-black uppercase tracking-widest">Active Reliability Plan</h3>
        </div>
      </div>
      <BaseTable :columns="columns" :data="maintenanceStore.pmSchedules">
        <template #cell(interval_days)="{ row }">
          <span class="text-xs font-bold">{{ row.interval_days }} Days</span>
        </template>
        <template #cell(next_due_at)="{ row }">
          <span class="text-xs text-muted-foreground">{{ row.next_due_at ? new Date(row.next_due_at).toLocaleDateString() : 'N/A' }}</span>
        </template>
        <template #cell(is_active)="{ row }">
          <span :class="['px-2 py-0.5 rounded text-[10px] font-bold uppercase', row.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700']">
            {{ row.is_active ? 'Active' : 'Disabled' }}
          </span>
        </template>
        <template #empty>
          <div class="py-16 text-center text-muted-foreground italic text-xs">
            No preventive maintenance schedules defined.
          </div>
        </template>
      </BaseTable>
    </div>
  </div>
</template>
