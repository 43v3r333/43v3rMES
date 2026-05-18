<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useAnalyticsStore } from '@/stores/analytics'
import BaseTable from '@/components/ui/BaseTable.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import { BarChart3, TrendingUp, AlertCircle, Filter, Download } from 'lucide-vue-next'

const analyticsStore = useAnalyticsStore()

const agingColumns = [
  { key: 'event_number', label: 'ID' },
  { key: 'title', label: 'Description' },
  { key: 'age_hours', label: 'Age (hrs)' },
  { key: 'severity', label: 'Severity' },
]

onMounted(() => {
  analyticsStore.fetchKPIs()
  analyticsStore.fetchPareto()
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Operational Intelligence</h1>
        <p class="text-sm text-muted-foreground uppercase font-bold tracking-tighter">Performance & Reliability Analytics</p>
      </div>
      <div class="flex items-center space-x-2">
        <BaseButton variant="outline" class="h-9">
          <Filter class="mr-2 h-4 w-4" />
          Analytics Period
        </BaseButton>
        <BaseButton variant="primary" class="h-9">
          <Download class="mr-2 h-4 w-4" />
          Export Dataset
        </BaseButton>
      </div>
    </div>

    <!-- KPI Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
      <div v-for="(val, label) in {
        'MTTR': '42m',
        'MTBF': '124h',
        'Availability': '98.2%',
        'Downtime %': '1.8%',
        'Open Issues': '14',
        'Escalations': '2'
      }" :key="label" class="p-4 bg-card border rounded-lg shadow-sm">
        <div class="text-[10px] font-bold text-muted-foreground uppercase tracking-wider">{{ label }}</div>
        <div class="mt-1 text-xl font-extrabold tracking-tight">{{ val }}</div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Pareto Analysis -->
      <div class="bg-card border rounded-lg shadow-sm">
        <div class="p-4 border-b bg-muted/20 flex items-center justify-between">
          <div class="flex items-center">
            <BarChart3 class="mr-2 h-4 w-4 text-primary" />
            <h3 class="font-bold text-sm uppercase tracking-wider">Downtime Pareto (by Category)</h3>
          </div>
        </div>
        <div class="p-6 h-[300px] flex items-center justify-center border-dashed border-2 m-4 rounded bg-muted/5 text-muted-foreground text-xs font-mono">
          [ ECharts: Pareto Implementation ]
        </div>
      </div>

      <!-- Trend Analysis -->
      <div class="bg-card border rounded-lg shadow-sm">
        <div class="p-4 border-b bg-muted/20 flex items-center justify-between">
          <div class="flex items-center">
            <TrendingUp class="mr-2 h-4 w-4 text-primary" />
            <h3 class="font-bold text-sm uppercase tracking-wider">Availability Trend</h3>
          </div>
        </div>
        <div class="p-6 h-[300px] flex items-center justify-center border-dashed border-2 m-4 rounded bg-muted/5 text-muted-foreground text-xs font-mono">
          [ ECharts: Multi-Series Trend ]
        </div>
      </div>
    </div>

    <!-- Aging Issues Table -->
    <div class="bg-card border rounded-lg shadow-sm">
      <div class="p-4 border-b bg-muted/20 flex items-center justify-between">
        <div class="flex items-center">
          <AlertCircle class="mr-2 h-4 w-4 text-red-500" />
          <h3 class="font-bold text-sm uppercase tracking-wider">Chronic & Aging Issues</h3>
        </div>
        <span class="text-[10px] font-bold text-red-600 bg-red-100 px-2 py-0.5 rounded">Action Required</span>
      </div>
      <BaseTable :columns="agingColumns" :data="analyticsStore.openIssues">
        <template #empty>
          <div class="py-12 text-center text-muted-foreground italic text-xs">
            No issues currently exceeding the aging threshold (24h).
          </div>
        </template>
      </BaseTable>
    </div>
  </div>
</template>
