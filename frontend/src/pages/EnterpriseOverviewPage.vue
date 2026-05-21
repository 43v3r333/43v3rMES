<script setup lang="ts">
import { onMounted } from 'vue'
import { useEnterpriseStore } from '@/stores/enterprise'
import BaseTable from '@/components/ui/BaseTable.vue'
import EnterpriseBadge from '@/components/enterprise/EnterpriseBadge.vue'
import { Globe, Map, BarChart2, AlertCircle, TrendingUp, TrendingDown, Activity } from 'lucide-vue-next'

const enterpriseStore = useEnterpriseStore()

const siteColumns = [
  { key: 'site_name', label: 'Manufacturing Node' },
  { key: 'region_name', label: 'Region' },
  { key: 'availability', label: 'Availability' },
  { key: 'mttr', label: 'MTTR' },
  { key: 'open_incidents', label: 'Incidents' },
]

onMounted(() => {
  enterpriseStore.fetchEnterpriseData()
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="h-10 w-10 bg-primary/10 rounded flex items-center justify-center text-primary">
          <Globe class="h-6 w-6" />
        </div>
        <div>
          <h1 class="text-2xl font-bold tracking-tight">Enterprise Multi-Site Operations</h1>
          <p class="text-sm text-muted-foreground uppercase font-black tracking-tighter">Global Manufacturing Intelligence</p>
        </div>
      </div>
    </div>

    <!-- Enterprise KPI Strip -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-card border rounded-lg p-6 shadow-sm flex flex-col justify-between">
        <div class="flex justify-between items-start">
          <div class="text-[10px] font-black uppercase text-muted-foreground tracking-widest">Global Availability</div>
          <TrendingUp class="h-4 w-4 text-green-500" />
        </div>
        <div class="mt-4 flex items-end space-x-2">
          <span class="text-4xl font-black tracking-tighter">{{ enterpriseStore.overview?.enterprise_availability }}%</span>
          <span class="text-[10px] font-bold text-green-600 mb-1">+0.2% vs PW</span>
        </div>
      </div>
      <div class="bg-card border rounded-lg p-6 shadow-sm flex flex-col justify-between">
        <div class="flex justify-between items-start">
          <div class="text-[10px] font-black uppercase text-muted-foreground tracking-widest">Active Incidents (All Sites)</div>
          <Activity class="h-4 w-4 text-red-500" />
        </div>
        <div class="mt-4 flex items-end space-x-2">
          <span class="text-4xl font-black tracking-tighter">{{ enterpriseStore.overview?.active_incidents_total }}</span>
          <span class="text-[10px] font-bold text-red-600 mb-1">Critical: {{ enterpriseStore.overview?.critical_risk_sites }}</span>
        </div>
      </div>
      <div class="bg-card border rounded-lg p-6 shadow-sm flex flex-col justify-between">
        <div class="text-[10px] font-black uppercase text-muted-foreground tracking-widest mb-4">Top Performing Node</div>
        <div class="text-xl font-black text-primary uppercase">{{ enterpriseStore.overview?.top_performing_site }}</div>
        <div class="mt-1 text-[10px] font-bold text-muted-foreground">OEE: 98.2% | MTBF: 142h</div>
      </div>
      <div class="bg-card border rounded-lg p-6 shadow-sm flex flex-col justify-between">
        <div class="text-[10px] font-black uppercase text-muted-foreground tracking-widest mb-4">Regional Distribution</div>
        <div class="flex items-center space-x-2">
          <Map class="h-4 w-4 text-primary" />
          <span class="text-xs font-bold uppercase tracking-tight">4 Regions Active</span>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      <!-- Site Comparison Table -->
      <div class="lg:col-span-8 bg-card border rounded-lg shadow-sm">
        <div class="p-4 border-b bg-muted/20 flex items-center justify-between">
          <div class="flex items-center">
            <BarChart2 class="mr-2 h-4 w-4 text-primary" />
            <h3 class="text-xs font-black uppercase tracking-widest">Cross-Site Benchmarking</h3>
          </div>
        </div>
        <BaseTable :columns="siteColumns" :data="enterpriseStore.siteComparisons">
          <template #cell(site_name)="{ row }">
            <span class="font-bold text-xs uppercase">{{ row.site_name }}</span>
          </template>
          <template #cell(region_name)="{ row }">
            <span class="text-[10px] font-bold text-muted-foreground uppercase">{{ row.region_name }}</span>
          </template>
          <template #cell(availability)="{ row }">
            <div class="flex items-center space-x-2">
              <span class="font-mono text-xs font-bold">{{ row.availability }}%</span>
              <div class="w-16 h-1.5 bg-muted rounded-full overflow-hidden">
                <div class="h-full bg-primary" :style="{ width: row.availability + '%' }"></div>
              </div>
            </div>
          </template>
          <template #cell(open_incidents)="{ row }">
            <EnterpriseBadge :variant="row.open_incidents > 10 ? 'error' : 'warning'">
              {{ row.open_incidents }} Active
            </EnterpriseBadge>
          </template>
        </BaseTable>
      </div>

      <!-- Enterprise Alert Feed -->
      <div class="lg:col-span-4 space-y-4">
        <div class="bg-card border rounded-lg shadow-sm flex flex-col h-full">
          <div class="p-4 border-b bg-muted/20 flex items-center">
            <AlertCircle class="mr-2 h-4 w-4 text-red-500" />
            <h3 class="text-xs font-black uppercase tracking-widest text-red-600">Enterprise Escalations</h3>
          </div>
          <div class="p-4 space-y-3 flex-1 overflow-y-auto">
            <div v-for="i in 5" :key="i" class="p-3 border-l-4 border-l-red-500 bg-red-500/5 rounded shadow-sm space-y-1">
              <div class="flex justify-between items-center text-[9px] font-black uppercase">
                <span>Site: 43v3r-Gamma</span>
                <span class="text-muted-foreground">12m Ago</span>
              </div>
              <p class="text-xs font-bold leading-tight">Critical Power Loss reported across Production Area 4.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
