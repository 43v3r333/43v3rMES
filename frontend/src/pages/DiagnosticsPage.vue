<script setup lang="ts">
import { ref } from 'vue'
import BaseButton from '@/components/enterprise/EnterpriseButton.vue'
import EnterpriseBadge from '@/components/enterprise/EnterpriseBadge.vue'
import { Activity, ShieldCheck, Database, Zap, HardDrive, Search } from 'lucide-vue-next'

const services = ref([
  { name: 'Core API', status: 'Healthy', latency: '12ms', icon: Activity },
  { name: 'PostgreSQL', status: 'Healthy', latency: '4ms', icon: Database },
  { name: 'Redis Cache', status: 'Healthy', latency: '1ms', icon: Zap },
  { name: 'Blob Storage', status: 'Healthy', latency: '42ms', icon: HardDrive },
  { name: 'Search Index', status: 'Healthy', latency: '8ms', icon: Search },
])
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">System Diagnostics</h1>
        <p class="text-sm text-muted-foreground uppercase font-black tracking-tighter">Enterprise Platform Integrity</p>
      </div>
      <BaseButton variant="primary">Run Deep Validation</BaseButton>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="s in services" :key="s.name" class="bg-card border rounded-lg p-5 shadow-sm flex flex-col space-y-4">
        <div class="flex justify-between items-start">
          <div class="h-10 w-10 bg-primary/10 rounded flex items-center justify-center text-primary">
            <component :is="s.icon" class="h-5 w-5" />
          </div>
          <EnterpriseBadge variant="success">{{ s.status }}</EnterpriseBadge>
        </div>
        <div>
          <h3 class="text-xs font-black uppercase tracking-widest">{{ s.name }}</h3>
          <p class="text-[10px] text-muted-foreground font-bold">Node Latency: {{ s.latency }}</p>
        </div>
        <div class="pt-2 border-t border-dashed flex justify-between items-center text-[9px] font-black uppercase text-muted-foreground">
          <span>Uptime: 99.998%</span>
          <button class="hover:text-primary underline">Logs</button>
        </div>
      </div>
    </div>

    <div class="bg-card border rounded-lg shadow-sm p-6 space-y-4">
      <div class="flex items-center space-x-2 border-b pb-4">
        <ShieldCheck class="h-5 w-5 text-green-500" />
        <h3 class="text-sm font-black uppercase tracking-widest">Environment Validation</h3>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div v-for="i in ['JWT Config', 'CORS Policy', 'Tenant Isolation', 'RBAC Foundation']" :key="i"
             class="p-3 bg-muted/20 rounded border flex flex-col items-center text-center space-y-2">
          <span class="text-[10px] font-black uppercase">{{ i }}</span>
          <EnterpriseBadge variant="success">Verified</EnterpriseBadge>
        </div>
      </div>
    </div>
  </div>
</template>
