<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useDowntimeStore } from '@/stores/downtime'
import BaseTable from '@/components/ui/BaseTable.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { Plus, Filter, Search, AlertTriangle, Clock, CheckCircle2 } from 'lucide-vue-next'

const downtimeStore = useDowntimeStore()

const columns = [
  { key: 'event_number', label: 'ID' },
  { key: 'status', label: 'Status' },
  { key: 'severity', label: 'Severity' },
  { key: 'title', label: 'Incident Title' },
  { key: 'started_at', label: 'Started' },
  { key: 'duration_minutes', label: 'Duration' },
]

onMounted(() => {
  downtimeStore.fetchEvents()
})

const getStatusClass = (status: string) => {
  switch (status) {
    case 'OPEN': return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
    case 'IN_PROGRESS': return 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400'
    case 'RESOLVED': return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'
    default: return 'bg-muted text-muted-foreground'
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Downtime Management</h1>
        <p class="text-sm text-muted-foreground italic uppercase tracking-wider font-semibold">Operational Incident Log</p>
      </div>
      <div class="flex items-center space-x-2">
        <BaseButton variant="outline" class="h-9 px-3">
          <Filter class="mr-2 h-4 w-4" />
          Filter
        </BaseButton>
        <BaseButton variant="primary" class="h-9 px-3">
          <Plus class="mr-2 h-4 w-4" />
          Report Incident
        </BaseButton>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div class="p-4 bg-card border rounded flex items-center space-x-4">
        <div class="p-2 bg-red-100 text-red-600 rounded">
          <AlertTriangle class="h-5 w-5" />
        </div>
        <div>
          <div class="text-xs font-bold text-muted-foreground uppercase">Unresolved</div>
          <div class="text-xl font-bold">12 Issues</div>
        </div>
      </div>
      <div class="p-4 bg-card border rounded flex items-center space-x-4">
        <div class="p-2 bg-amber-100 text-amber-600 rounded">
          <Clock class="h-5 w-5" />
        </div>
        <div>
          <div class="text-xs font-bold text-muted-foreground uppercase">MTTR</div>
          <div class="text-xl font-bold">42 Minutes</div>
        </div>
      </div>
      <div class="p-4 bg-card border rounded flex items-center space-x-4">
        <div class="p-2 bg-green-100 text-green-600 rounded">
          <CheckCircle2 class="h-5 w-5" />
        </div>
        <div>
          <div class="text-xs font-bold text-muted-foreground uppercase">Uptime Score</div>
          <div class="text-xl font-bold">98.4%</div>
        </div>
      </div>
    </div>

    <div class="bg-card border rounded-lg shadow-sm">
      <div class="p-4 border-b flex items-center justify-between bg-muted/20">
        <div class="relative w-full max-w-sm">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search events, machines, or root causes..."
            class="w-full pl-9 pr-4 py-2 bg-background border rounded-md text-sm outline-none focus:ring-1 focus:ring-primary"
          />
        </div>
      </div>

      <BaseTable :columns="columns" :data="downtimeStore.events">
        <template #cell(event_number)="{ row }">
          <span class="font-mono font-bold text-xs">{{ row.event_number }}</span>
        </template>
        <template #cell(status)="{ row }">
          <span :class="['px-2 py-0.5 rounded-[4px] text-[10px] font-bold tracking-tighter', getStatusClass(row.status)]">
            {{ row.status }}
          </span>
        </template>
        <template #cell(severity)="{ row }">
          <span
            class="text-[10px] font-bold uppercase tracking-tighter"
            :class="row.severity === 'CRITICAL' ? 'text-red-600' : 'text-muted-foreground'"
          >
            {{ row.severity }}
          </span>
        </template>
        <template #cell(started_at)="{ row }">
          <span class="text-xs text-muted-foreground">{{ new Date(row.started_at).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' }) }}</span>
        </template>
        <template #cell(duration_minutes)="{ row }">
          <span class="font-mono font-semibold">{{ row.duration_minutes || '-' }}m</span>
        </template>
        <template #empty>
          <div class="py-16 text-center text-muted-foreground">
            No downtime incidents reported in the current period.
          </div>
        </template>
      </BaseTable>
    </div>
  </div>
</template>
