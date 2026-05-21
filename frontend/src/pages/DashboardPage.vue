<script setup lang="ts">
import BaseTable from '@/components/ui/BaseTable.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const recentEvents = [
  { id: 1, machine: 'IM-001', event: 'Maintenance', duration: '2h 15m', status: 'In Progress' },
  { id: 2, machine: 'IM-003', event: 'Power Loss', duration: '45m', status: 'Resolved' },
  { id: 3, machine: 'PK-012', event: 'Jam', duration: '12m', status: 'Resolved' },
]

const columns = [
  { key: 'machine', label: 'Machine ID' },
  { key: 'event', label: 'Event Type' },
  { key: 'duration', label: 'Duration' },
  { key: 'status', label: 'Status' },
]
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold tracking-tight">Operational Overview</h1>
      <BaseButton variant="primary">Generate Report</BaseButton>
    </div>

    <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <div v-for="i in 4" :key="i" class="p-6 bg-card border rounded-lg shadow-sm">
        <div class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">KPI Segment {{ i }}</div>
        <div class="mt-2 text-3xl font-bold tracking-tighter">98.{{ i }}%</div>
        <div class="mt-2 text-xs text-green-500 font-medium flex items-center">
          +0.4% from target
        </div>
      </div>
    </div>

    <div class="bg-card border rounded-lg shadow-sm">
      <div class="p-4 border-b">
        <h3 class="font-semibold">Recent Downtime Events</h3>
      </div>
      <BaseTable :columns="columns" :data="recentEvents">
        <template #cell(status)="{ row }">
          <span
            :class="[
              'px-2 py-1 rounded text-xs font-bold uppercase',
              row.status === 'Resolved' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'
            ]"
          >
            {{ row.status }}
          </span>
        </template>
      </BaseTable>
    </div>
  </div>
</template>
