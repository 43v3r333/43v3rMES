<script setup lang="ts">
import { onMounted } from 'vue'
import { useMaintenanceStore } from '@/stores/maintenance'
import BaseTable from '@/components/ui/BaseTable.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { Plus, Wrench, Clock, UserCheck, AlertTriangle } from 'lucide-vue-next'

const maintenanceStore = useMaintenanceStore()

const columns = [
  { key: 'work_order_number', label: 'WO#' },
  { key: 'status', label: 'Status' },
  { key: 'priority', label: 'Priority' },
  { key: 'title', label: 'Maintenance Task' },
  { key: 'machine_id', label: 'Asset' },
  { key: 'due_date', label: 'Due Date' },
]

onMounted(() => {
  maintenanceStore.fetchWorkOrders()
})

const getStatusClass = (status: string) => {
  switch (status) {
    case 'OPEN': return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30'
    case 'IN_PROGRESS': return 'bg-amber-100 text-amber-700 dark:bg-amber-900/30'
    case 'COMPLETED': return 'bg-green-100 text-green-700 dark:bg-green-900/30'
    case 'WAITING_PARTS': return 'bg-purple-100 text-purple-700'
    default: return 'bg-muted text-muted-foreground'
  }
}

const getPriorityClass = (priority: string) => {
  switch (priority) {
    case 'EMERGENCY': return 'text-red-600 font-black animate-pulse'
    case 'HIGH': return 'text-orange-600 font-bold'
    default: return 'text-muted-foreground'
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Maintenance Work Orders</h1>
        <p class="text-sm text-muted-foreground uppercase font-black tracking-tighter">Execution & Service Log</p>
      </div>
      <BaseButton variant="primary">
        <Plus class="mr-2 h-4 w-4" />
        New Work Order
      </BaseButton>
    </div>

    <!-- Maintenance Overview -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-card border p-4 rounded shadow-sm flex items-center space-x-4">
        <div class="p-2 bg-blue-100 text-blue-600 rounded">
          <Wrench class="h-5 w-5" />
        </div>
        <div>
          <div class="text-[10px] font-bold text-muted-foreground uppercase">Active WOs</div>
          <div class="text-lg font-black">24</div>
        </div>
      </div>
      <div class="bg-card border p-4 rounded shadow-sm flex items-center space-x-4">
        <div class="p-2 bg-red-100 text-red-600 rounded">
          <AlertTriangle class="h-5 w-5" />
        </div>
        <div>
          <div class="text-[10px] font-bold text-muted-foreground uppercase">Overdue</div>
          <div class="text-lg font-black text-red-600">3</div>
        </div>
      </div>
      <div class="bg-card border p-4 rounded shadow-sm flex items-center space-x-4">
        <div class="p-2 bg-amber-100 text-amber-600 rounded">
          <Clock class="h-5 w-5" />
        </div>
        <div>
          <div class="text-[10px] font-bold text-muted-foreground uppercase">Avg Resolution</div>
          <div class="text-lg font-black">4.2h</div>
        </div>
      </div>
      <div class="bg-card border p-4 rounded shadow-sm flex items-center space-x-4">
        <div class="p-2 bg-green-100 text-green-600 rounded">
          <UserCheck class="h-5 w-5" />
        </div>
        <div>
          <div class="text-[10px] font-bold text-muted-foreground uppercase">Staff Utility</div>
          <div class="text-lg font-black">88%</div>
        </div>
      </div>
    </div>

    <div class="bg-card border rounded-lg shadow-sm">
      <div class="p-4 border-b bg-muted/20 flex items-center justify-between">
        <h3 class="text-xs font-black uppercase tracking-widest">Active Maintenance Queue</h3>
      </div>
      <BaseTable :columns="columns" :data="maintenanceStore.workOrders">
        <template #cell(work_order_number)="{ row }">
          <span class="font-mono text-xs font-bold text-primary">{{ row.work_order_number }}</span>
        </template>
        <template #cell(status)="{ row }">
          <span :class="['px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-tighter', getStatusClass(row.status)]">
            {{ row.status }}
          </span>
        </template>
        <template #cell(priority)="{ row }">
          <span :class="['text-[10px] font-black uppercase tracking-tighter', getPriorityClass(row.priority)]">
            {{ row.priority }}
          </span>
        </template>
        <template #cell(due_date)="{ row }">
          <span class="text-xs text-muted-foreground">{{ row.due_date ? new Date(row.due_date).toLocaleDateString() : 'No Date' }}</span>
        </template>
        <template #empty>
          <div class="py-16 text-center text-muted-foreground italic text-xs">
            No active work orders in the maintenance queue.
          </div>
        </template>
      </BaseTable>
    </div>
  </div>
</template>
