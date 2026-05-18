<script setup lang="ts">
import { onMounted } from 'vue'
import { useNotificationStore } from '@/stores/notification'
import { Bell, Check, AlertTriangle, Info, Clock } from 'lucide-vue-next'

const notificationStore = useNotificationStore()

onMounted(() => {
  notificationStore.fetchNotifications()
})

const getIcon = (type: string) => {
  switch (type) {
    case 'ESCALATION': return AlertTriangle
    case 'ASSIGNMENT': return Info
    default: return Bell
  }
}

const getSeverityClass = (severity: string) => {
  switch (severity) {
    case 'CRITICAL': return 'text-red-500'
    case 'HIGH': return 'text-amber-500'
    default: return 'text-primary'
  }
}
</script>

<template>
  <div class="w-80 bg-card border rounded-lg shadow-xl overflow-hidden flex flex-col max-h-[500px]">
    <div class="p-4 border-b bg-muted/20 flex items-center justify-between">
      <h3 class="font-bold text-xs uppercase tracking-widest">Operational Alerts</h3>
      <span v-if="notificationStore.unreadCount > 0" class="bg-primary text-primary-foreground text-[10px] px-2 py-0.5 rounded-full font-bold">
        {{ notificationStore.unreadCount }} New
      </span>
    </div>
    <div class="flex-1 overflow-y-auto">
      <div v-for="n in notificationStore.notifications" :key="n.id"
           :class="['p-4 border-b hover:bg-muted/30 transition-colors relative cursor-pointer', !n.is_read ? 'bg-primary/5' : '']"
           @click="notificationStore.markAsRead(n.id)">
        <div class="flex space-x-3">
          <div :class="['mt-1', getSeverityClass(n.severity)]">
            <component :is="getIcon(n.type)" class="h-4 w-4" />
          </div>
          <div class="flex-1 space-y-1">
            <div class="flex items-center justify-between">
              <span :class="['text-xs font-bold', !n.is_read ? 'text-foreground' : 'text-muted-foreground']">{{ n.title }}</span>
              <span class="text-[10px] text-muted-foreground flex items-center italic">
                <Clock class="h-2 w-2 mr-1" />
                {{ new Date(n.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}
              </span>
            </div>
            <p class="text-xs text-muted-foreground line-clamp-2 leading-relaxed">{{ n.message }}</p>
          </div>
        </div>
        <div v-if="!n.is_read" class="absolute left-0 top-0 bottom-0 w-0.5 bg-primary"></div>
      </div>
      <div v-if="notificationStore.notifications.length === 0" class="py-12 text-center text-xs text-muted-foreground italic">
        No active notifications.
      </div>
    </div>
    <div class="p-2 border-t bg-muted/10 text-center">
      <button class="text-[10px] font-bold uppercase text-primary hover:underline">Clear All Notifications</button>
    </div>
  </div>
</template>
