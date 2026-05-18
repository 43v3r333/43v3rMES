<script setup lang="ts">
import { Clock, User, CheckCircle } from 'lucide-vue-next'

defineProps<{
  events: { type: string; user: string; time: string; content: string }[];
}>();
</script>

<template>
  <div class="space-y-4">
    <div v-for="(event, i) in events" :key="i" class="flex space-x-3">
      <div class="flex flex-col items-center">
        <div class="h-8 w-8 rounded-full bg-muted flex items-center justify-center">
          <component :is="event.type === 'comment' ? User : CheckCircle" class="h-4 w-4" />
        </div>
        <div v-if="i < events.length - 1" class="w-px flex-1 bg-border my-1"></div>
      </div>
      <div class="pb-4">
        <div class="flex items-center space-x-2 text-xs">
          <span class="font-bold text-foreground">{{ event.user }}</span>
          <span class="text-muted-foreground">{{ event.time }}</span>
        </div>
        <div class="mt-1 p-2 bg-muted/50 rounded text-sm border">
          {{ event.content }}
        </div>
      </div>
    </div>
  </div>
</template>
