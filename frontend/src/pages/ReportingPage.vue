<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useReportingStore } from '@/stores/reporting'
import BaseTable from '@/components/ui/BaseTable.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { FileBarChart, Download, Clock, Filter, Save, FileText } from 'lucide-vue-next'

const reportingStore = useReportingStore()

const historyColumns = [
  { key: 'report_type', label: 'Report Type' },
  { key: 'format', label: 'Format' },
  { key: 'status', label: 'Status' },
  { key: 'started_at', label: 'Generated At' },
]

onMounted(() => {
  reportingStore.fetchTemplates()
  reportingStore.fetchExportHistory()
})

const getStatusClass = (status: string) => {
  switch (status) {
    case 'COMPLETED': return 'bg-green-100 text-green-700'
    case 'PENDING': return 'bg-blue-100 text-blue-700 animate-pulse'
    case 'FAILED': return 'bg-red-100 text-red-700'
    default: return 'bg-muted text-muted-foreground'
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Reporting & Exports</h1>
        <p class="text-sm text-muted-foreground uppercase font-black tracking-tighter">Operational Documentation Engine</p>
      </div>
      <BaseButton variant="primary">
        <FileBarChart class="mr-2 h-4 w-4" />
        Build New Report
      </BaseButton>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Report Templates / Builder -->
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-card border rounded-lg shadow-sm">
          <div class="p-4 border-b bg-muted/20 flex items-center justify-between">
            <div class="flex items-center">
              <FileText class="mr-2 h-4 w-4 text-primary" />
              <h3 class="text-xs font-black uppercase tracking-widest">Standardized Templates</h3>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
            <div v-for="type in ['Shift Summary', 'Maintenance Activity', 'Downtime Pareto', 'KPI Performance', 'Escalation History']" :key="type"
                 class="p-4 border rounded hover:border-primary cursor-pointer transition-colors flex items-center justify-between bg-muted/5 group">
              <span class="text-xs font-bold uppercase tracking-tight">{{ type }}</span>
              <Download class="h-4 w-4 text-muted-foreground group-hover:text-primary" />
            </div>
          </div>
        </div>

        <!-- Export History -->
        <div class="bg-card border rounded-lg shadow-sm">
          <div class="p-4 border-b bg-muted/20 flex items-center justify-between">
            <div class="flex items-center">
              <Clock class="mr-2 h-4 w-4 text-primary" />
              <h3 class="text-xs font-black uppercase tracking-widest">Recent Export History</h3>
            </div>
          </div>
          <BaseTable :columns="historyColumns" :data="reportingStore.exportHistory">
            <template #cell(report_type)="{ row }">
              <span class="text-[11px] font-bold uppercase">{{ row.report_type }}</span>
            </template>
            <template #cell(status)="{ row }">
              <span :class="['px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-tighter', getStatusClass(row.status)]">
                {{ row.status }}
              </span>
            </template>
            <template #cell(started_at)="{ row }">
              <span class="text-xs text-muted-foreground">{{ new Date(row.started_at).toLocaleString() }}</span>
            </template>
            <template #empty>
              <div class="py-12 text-center text-muted-foreground italic text-xs">
                No recent export requests found.
              </div>
            </template>
          </BaseTable>
        </div>
      </div>

      <!-- Quick Filters / Sidebar -->
      <div class="space-y-4">
        <div class="bg-card border rounded-lg shadow-sm">
          <div class="p-4 border-b bg-muted/20 flex items-center">
            <Save class="mr-2 h-4 w-4 text-primary" />
            <h3 class="text-xs font-black uppercase tracking-widest">Saved Configurations</h3>
          </div>
          <div class="p-4 space-y-2">
            <div v-for="t in reportingStore.templates" :key="t.id" class="p-2 border rounded text-xs font-medium hover:bg-muted/30 cursor-pointer">
              {{ t.name }}
            </div>
            <div v-if="reportingStore.templates.length === 0" class="text-center py-8 text-xs text-muted-foreground italic">
              No saved filter sets.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
