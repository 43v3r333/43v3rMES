<script setup lang="ts">
import { onMounted } from 'vue'
import { useWorkflowStore } from '@/stores/workflow'
import BaseTable from '@/components/ui/BaseTable.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { Plus, ArrowRightLeft, FileText, ClipboardList } from 'lucide-vue-next'

const workflowStore = useWorkflowStore()

const columns = [
  { key: 'date', label: 'Date' },
  { key: 'outgoing_shift_id', label: 'Outgoing' },
  { key: 'incoming_shift_id', label: 'Incoming' },
  { key: 'supervisor_id', label: 'Supervisor' },
]

onMounted(() => {
  workflowStore.fetchHandovers()
  workflowStore.fetchShifts()
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Shift Handovers</h1>
        <p class="text-sm text-muted-foreground uppercase font-bold tracking-tighter">Operational Continuity Log</p>
      </div>
      <BaseButton variant="primary">
        <ArrowRightLeft class="mr-2 h-4 w-4" />
        New Handover
      </BaseButton>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Recent Handovers List -->
      <div class="lg:col-span-2 space-y-4">
        <div class="bg-card border rounded-lg shadow-sm">
          <div class="p-4 border-b bg-muted/20 flex items-center">
            <ClipboardList class="mr-2 h-4 w-4 text-primary" />
            <h3 class="font-bold text-sm uppercase tracking-wider">Handover History</h3>
          </div>
          <BaseTable :columns="columns" :data="workflowStore.handovers">
            <template #cell(date)="{ row }">
              <span class="font-medium">{{ new Date(row.date).toLocaleDateString() }}</span>
            </template>
            <template #cell(supervisor_id)="{ row }">
              <span class="text-xs font-mono">{{ row.supervisor_id.split('-')[0] }}...</span>
            </template>
            <template #empty>
              <div class="py-12 text-center text-muted-foreground">
                No handover records found.
              </div>
            </template>
          </BaseTable>
        </div>
      </div>

      <!-- Operational Queue / Carryover Sidebar -->
      <div class="space-y-4">
        <div class="bg-card border rounded-lg shadow-sm">
          <div class="p-4 border-b bg-muted/20 flex items-center">
            <FileText class="mr-2 h-4 w-4 text-amber-500" />
            <h3 class="font-bold text-sm uppercase tracking-wider text-amber-600">Pending Issues</h3>
          </div>
          <div class="p-4 space-y-3">
            <div v-for="i in 3" :key="i" class="p-3 border rounded bg-muted/10">
              <div class="flex justify-between items-start">
                <span class="text-[10px] font-bold bg-amber-100 text-amber-700 px-1 rounded">DT-00{{ i }}</span>
                <span class="text-[10px] text-muted-foreground">Shift Carryover</span>
              </div>
              <p class="mt-2 text-xs font-medium line-clamp-2">Mechanical issue with Production Line A - Roller Jam</p>
              <div class="mt-2 flex items-center text-[10px] text-muted-foreground italic">
                Active for 4h 12m
              </div>
            </div>
            <BaseButton variant="outline" class="w-full text-xs h-8">View All Pending</BaseButton>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
