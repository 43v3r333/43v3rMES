<script setup lang="ts">
import { ref } from 'vue'
import BaseTable from '@/components/ui/BaseTable.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { Settings, ShieldAlert, Plus, Zap } from 'lucide-vue-next'

const rules = ref([
  { id: 1, name: 'Critical Downtime Escalation', entity: 'DowntimeEvent', condition: 'Duration > 30m', target: 'Plant Manager', status: 'Active' },
  { id: 2, name: 'Repeated Machine Failure', entity: 'Machine', condition: 'Count > 3 / Shift', target: 'Maintenance Lead', status: 'Active' },
])

const columns = [
  { key: 'name', label: 'Rule Name' },
  { key: 'entity', label: 'Trigger Entity' },
  { key: 'condition', label: 'Threshold Condition' },
  { key: 'target', label: 'Escalation Path' },
  { key: 'status', label: 'Status' },
]
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Escalation Workflows</h1>
        <p class="text-sm text-muted-foreground uppercase font-bold tracking-tighter">Automated Accountability Engine</p>
      </div>
      <BaseButton variant="primary">
        <Plus class="mr-2 h-4 w-4" />
        Define Rule
      </BaseButton>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-card border rounded-lg p-6 shadow-sm flex items-center space-x-4">
        <div class="p-3 bg-primary/10 text-primary rounded">
          <ShieldAlert class="h-6 w-6" />
        </div>
        <div>
          <div class="text-xs font-bold text-muted-foreground uppercase">Active Rules</div>
          <div class="text-2xl font-extrabold tracking-tighter">14 Workflows</div>
        </div>
      </div>
      <div class="bg-card border rounded-lg p-6 shadow-sm flex items-center space-x-4">
        <div class="p-3 bg-amber-100 text-amber-600 rounded">
          <Zap class="h-6 w-6" />
        </div>
        <div>
          <div class="text-xs font-bold text-muted-foreground uppercase">Escalations (24h)</div>
          <div class="text-2xl font-extrabold tracking-tighter">3 Triggers</div>
        </div>
      </div>
    </div>

    <div class="bg-card border rounded-lg shadow-sm">
      <div class="p-4 border-b bg-muted/20 flex items-center justify-between">
        <div class="flex items-center">
          <Settings class="mr-2 h-4 w-4 text-primary" />
          <h3 class="font-bold text-sm uppercase tracking-wider">Enterprise Rule Engine</h3>
        </div>
      </div>
      <BaseTable :columns="columns" :data="rules">
        <template #cell(status)="{ row }">
          <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-green-100 text-green-700">{{ row.status }}</span>
        </template>
      </BaseTable>
    </div>
  </div>
</template>
