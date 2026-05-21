<script setup lang="ts">
import { onMounted } from 'vue'
import { useOperationsStore } from '@/stores/operations'
import BaseTable from '@/components/ui/BaseTable.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import {
  Radio,
  Activity,
  AlertCircle,
  Clock,
  Users,
  Maximize2,
  RefreshCcw,
  Zap
} from 'lucide-vue-next'

const operationsStore = useOperationsStore()

const incidentColumns = [
  { key: 'event_number', label: 'ID' },
  { key: 'severity', label: 'Sev' },
  { key: 'title', label: 'Incident' },
  { key: 'duration_minutes', label: 'Age' },
  { key: 'machines', label: 'Assets' },
]

onMounted(() => {
  operationsStore.fetchAll()
})

const getSeverityClass = (sev: string) => {
  switch (sev) {
    case 'CRITICAL': return 'text-red-500 font-black'
    case 'HIGH': return 'text-amber-500 font-bold'
    default: return 'text-muted-foreground'
  }
}
</script>

<template>
  <div class="h-full flex flex-col space-y-4">
    <!-- CommandCenter Header -->
    <div class="flex items-center justify-between bg-card border p-4 rounded-lg shadow-sm">
      <div class="flex items-center space-x-3">
        <div class="h-10 w-10 bg-primary/10 rounded flex items-center justify-center text-primary animate-pulse">
          <Radio class="h-6 w-6" />
        </div>
        <div>
          <h1 class="text-xl font-black uppercase tracking-tighter">Operations Command Center</h1>
          <div class="flex items-center space-x-3 text-[10px] font-bold text-muted-foreground uppercase">
            <span class="flex items-center text-green-500"><Zap class="h-3 w-3 mr-1" /> Live Feed</span>
            <span>Factory: 43v3r-Alpha</span>
            <span>Shift: {{ operationsStore.overview?.current_shift_name }}</span>
          </div>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <BaseButton variant="outline" class="h-9 font-bold text-xs uppercase" @click="operationsStore.fetchAll">
          <RefreshCcw class="h-3 w-3 mr-2" /> Force Refresh
        </BaseButton>
        <BaseButton variant="primary" class="h-9 font-bold text-xs uppercase">
          <Maximize2 class="h-3 w-3 mr-2" /> Fullscreen
        </BaseButton>
      </div>
    </div>

    <!-- KPI Strip -->
    <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
      <div v-for="(val, label) in {
        'Active Incidents': operationsStore.overview?.active_incident_count || 0,
        'Critical Alerts': operationsStore.overview?.critical_alert_count || 0,
        'MTTR (24h)': (operationsStore.overview?.mttr_last_24h || 0) + 'm',
        'Availability': (operationsStore.overview?.availability_score || 0) + '%',
        'Queue Age': '12m',
        'Throughput': '94%'
      }" :key="label" class="bg-card border p-3 rounded shadow-sm">
        <div class="text-[9px] font-black text-muted-foreground uppercase tracking-widest">{{ label }}</div>
        <div class="text-lg font-black tracking-tighter">{{ val }}</div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-4 flex-1 overflow-hidden">
      <!-- Active Incident Queue (Left) -->
      <div class="lg:col-span-8 flex flex-col min-h-0 bg-card border rounded-lg shadow-sm">
        <div class="p-3 border-b bg-muted/20 flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <Activity class="h-4 w-4 text-primary" />
            <h3 class="text-xs font-black uppercase tracking-widest">Active Incident Queue</h3>
          </div>
          <span class="text-[10px] font-bold text-muted-foreground italic">Sorting by Severity</span>
        </div>
        <div class="flex-1 overflow-auto p-2">
          <BaseTable :columns="incidentColumns" :data="operationsStore.activeIncidents">
            <template #cell(event_number)="{ row }">
              <span class="font-mono text-[11px] font-bold text-primary">{{ row.event_number }}</span>
            </template>
            <template #cell(severity)="{ row }">
              <span :class="['text-[10px] font-black uppercase', getSeverityClass(row.severity)]">{{ row.severity }}</span>
            </template>
            <template #cell(duration_minutes)="{ row }">
              <span class="font-mono text-xs font-bold">{{ row.duration_minutes }}m</span>
            </template>
            <template #cell(machines)="{ row }">
              <div class="flex flex-wrap gap-1">
                <span v-for="m in row.machines" :key="m" class="px-1.5 py-0.5 bg-muted border rounded text-[9px] font-bold">{{ m }}</span>
              </div>
            </template>
          </BaseTable>
        </div>
      </div>

      <!-- Operational Context (Right) -->
      <div class="lg:col-span-4 flex flex-col space-y-4">
        <!-- Shift Status -->
        <div class="bg-card border rounded-lg shadow-sm p-4">
          <div class="flex items-center space-x-2 mb-4 border-b pb-2">
            <Users class="h-4 w-4 text-primary" />
            <h3 class="text-xs font-black uppercase tracking-widest">Shift Context</h3>
          </div>
          <div class="space-y-3">
            <div class="flex justify-between items-center">
              <span class="text-[10px] font-bold text-muted-foreground uppercase">Supervisor</span>
              <span class="text-xs font-bold">{{ operationsStore.overview?.supervisor_on_duty }}</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-[10px] font-bold text-muted-foreground uppercase">Shift Ends In</span>
              <span class="text-xs font-bold text-amber-500">02h 14m</span>
            </div>
          </div>
        </div>

        <!-- Alert Feed -->
        <div class="bg-card border rounded-lg shadow-sm flex-1 flex flex-col min-h-0">
          <div class="p-3 border-b bg-muted/20 flex items-center">
            <AlertCircle class="h-4 w-4 text-red-500 mr-2" />
            <h3 class="text-xs font-black uppercase tracking-widest text-red-600">Priority Alerts</h3>
          </div>
          <div class="flex-1 overflow-y-auto p-3 space-y-2">
            <div v-for="i in 5" :key="i" class="p-2 border-l-2 border-red-500 bg-red-500/5 rounded-r">
              <div class="flex justify-between text-[9px] font-bold uppercase mb-1">
                <span class="text-red-600">Critical Escalation</span>
                <span class="text-muted-foreground">Just Now</span>
              </div>
              <p class="text-[11px] leading-tight font-medium">Production Line A roller jam has exceeded 30m resolution threshold.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
