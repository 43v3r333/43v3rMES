<script setup lang="ts">
import { History, User, Activity } from 'lucide-vue-next'

defineProps<{
  events: { action: string; entity: string; user: string; timestamp: string; reason?: string }[];
}>();
</script>

<template>
  <div class="bg-card border rounded-lg shadow-sm">
    <div class="p-4 border-b bg-muted/20 flex items-center justify-between">
      <div class="flex items-center">
        <History class="mr-2 h-4 w-4 text-primary" />
        <h3 class="font-bold text-sm uppercase tracking-wider">Operational Audit Trail</h3>
      </div>
      <span class="text-[10px] font-bold text-muted-foreground uppercase">Traceability Active</span>
    </div>
    <div class="p-4 space-y-4">
      <div v-for="(event, i) in events" :key="i" class="flex space-x-3">
        <div class="mt-1">
          <div class="h-6 w-6 rounded-full bg-muted flex items-center justify-center">
            <Activity class="h-3 w-3 text-muted-foreground" />
          </div>
        </div>
        <div class="flex-1 space-y-1">
          <div class="flex items-center justify-between">
            <span class="text-xs font-bold text-foreground">
              {{ event.user }} <span class="text-muted-foreground font-normal">performed</span> {{ event.action }}
            </span>
            <span class="text-[10px] text-muted-foreground">{{ event.timestamp }}</span>
          </div>
          <p class="text-xs text-muted-foreground italic">Target: {{ event.entity }}</p>
          <div v-if="event.reason" class="text-[10px] p-1 bg-muted rounded border border-dashed">
            Reason: {{ event.reason }}
          </div>
        </div>
      </div>
      <div v-if="events.length === 0" class="py-8 text-center text-xs text-muted-foreground">
        No audit events recorded for this context.
      </div>
    </div>
  </div>
</template>
