<script setup lang="ts">
import { onMounted } from 'vue'
import { useIntelligenceStore } from '@/stores/intelligence'
import EnterpriseBadge from '@/components/enterprise/EnterpriseBadge.vue'
import BaseButton from '@/components/enterprise/EnterpriseButton.vue'
import { BrainCircuit, Sparkles, AlertTriangle, ShieldCheck, Zap, ArrowRight, Lightbulb } from 'lucide-vue-next'

const intelligenceStore = useIntelligenceStore()

onMounted(() => {
  intelligenceStore.fetchIntelligence()
})

const getSeverityVariant = (sev: string) => {
  switch (sev) {
    case 'CRITICAL': return 'error'
    case 'HIGH': return 'warning'
    case 'MEDIUM': return 'info'
    default: return 'neutral'
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="h-10 w-10 bg-primary/10 rounded flex items-center justify-center text-primary">
          <BrainCircuit class="h-6 w-6" />
        </div>
        <div>
          <h1 class="text-2xl font-bold tracking-tight">Operational Intelligence</h1>
          <p class="text-sm text-muted-foreground uppercase font-black tracking-tighter">AI-Native Insight Engine</p>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <span class="text-[10px] font-bold text-muted-foreground uppercase flex items-center">
          <Sparkles class="h-3 w-3 mr-1 text-primary animate-pulse" />
          Real-time analysis active
        </span>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- AI Shift Summary -->
      <div class="lg:col-span-2 space-y-6">
        <div class="bg-card border rounded-lg shadow-sm overflow-hidden">
          <div class="p-4 border-b bg-muted/20 flex items-center justify-between">
            <div class="flex items-center">
              <Zap class="mr-2 h-4 w-4 text-primary" />
              <h3 class="text-xs font-black uppercase tracking-widest">Autonomous Shift Summary</h3>
            </div>
            <EnterpriseBadge :variant="intelligenceStore.latestSummary?.risk_level === 'HIGH' ? 'error' : 'success'">
              {{ intelligenceStore.latestSummary?.risk_level }} Risk
            </EnterpriseBadge>
          </div>
          <div class="p-6 space-y-6">
            <div class="prose prose-sm dark:prose-invert max-w-none">
              <p class="text-sm font-medium leading-relaxed italic border-l-4 border-primary/20 pl-4 py-1 bg-primary/5 rounded-r">
                "{{ intelligenceStore.latestSummary?.summary_text }}"
              </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-3">
                <h4 class="text-[10px] font-black uppercase tracking-widest text-muted-foreground flex items-center">
                  <AlertTriangle class="h-3 w-3 mr-1 text-amber-500" /> Key Issues Detected
                </h4>
                <ul class="space-y-2">
                  <li v-for="issue in intelligenceStore.latestSummary?.top_issues" :key="issue"
                      class="text-xs font-bold p-2 bg-muted/30 rounded border border-dashed flex items-center">
                    <ArrowRight class="h-3 w-3 mr-2 text-primary" /> {{ issue }}
                  </li>
                </ul>
              </div>
              <div class="space-y-3">
                <h4 class="text-[10px] font-black uppercase tracking-widest text-muted-foreground flex items-center">
                  <ShieldCheck class="h-3 w-3 mr-1 text-green-500" /> Maintenance Successes
                </h4>
                <ul class="space-y-2">
                  <li v-for="h in intelligenceStore.latestSummary?.maintenance_highlights" :key="h"
                      class="text-xs font-medium p-2 bg-green-500/5 rounded border border-green-500/10 flex items-center">
                    <ArrowRight class="h-3 w-3 mr-2 text-green-500" /> {{ h }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div class="p-3 border-t bg-muted/5 flex justify-between items-center px-6">
            <span class="text-[9px] font-bold text-muted-foreground uppercase">Analysis Confidence: {{ (intelligenceStore.latestSummary?.confidence || 0) * 100 }}%</span>
            <BaseButton variant="ghost" class="h-7 text-[10px] font-black uppercase">Regenerate Analysis</BaseButton>
          </div>
        </div>
      </div>

      <!-- Actionable Recommendations -->
      <div class="space-y-4">
        <div class="bg-card border rounded-lg shadow-sm flex flex-col h-full">
          <div class="p-4 border-b bg-muted/20 flex items-center">
            <Lightbulb class="mr-2 h-4 w-4 text-primary" />
            <h3 class="text-xs font-black uppercase tracking-widest">Operational Advice</h3>
          </div>
          <div class="p-4 space-y-4 flex-1 overflow-y-auto">
            <div v-for="rec in intelligenceStore.recommendations" :key="rec.id"
                 class="p-4 border rounded bg-card hover:bg-muted/10 transition-colors space-y-3 shadow-sm border-l-4"
                 :class="rec.severity === 'HIGH' ? 'border-l-amber-500' : 'border-l-primary'">
              <div class="flex justify-between items-start">
                <h4 class="text-xs font-black uppercase">{{ rec.title }}</h4>
                <EnterpriseBadge :variant="getSeverityVariant(rec.severity)">{{ rec.severity }}</EnterpriseBadge>
              </div>
              <p class="text-xs text-muted-foreground leading-tight">{{ rec.description }}</p>
              <div v-if="rec.action_item" class="p-2 bg-muted/30 rounded border border-dashed text-[10px] font-bold">
                Action: {{ rec.action_item }}
              </div>
              <BaseButton class="w-full h-8 text-[10px] font-black uppercase tracking-widest">Implement Advise</BaseButton>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
