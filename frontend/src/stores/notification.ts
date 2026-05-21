import { defineStore } from 'pinia'
import { ref } from 'vue'
import { notificationService } from '@/services/notification'
import type { Notification } from '@/types'

export const useNotificationStore = defineStore('notification', () => {
  const notifications = ref<Notification[]>([])
  const unreadCount = ref(0)
  const isLoading = ref(false)

  async function fetchNotifications() {
    isLoading.value = true
    try {
      notifications.value = await notificationService.getNotifications()
      const { count } = await notificationService.getUnreadCount()
      unreadCount.value = count
    } finally {
      isLoading.value = false
    }
  }

  async function markAsRead(id: string) {
    await notificationService.markRead(id)
    const notification = notifications.value.find(n => n.id === id)
    if (notification && !notification.is_read) {
      notification.is_read = true
      unreadCount.value = Math.max(0, unreadCount.value - 1)
    }
  }

  return { notifications, unreadCount, isLoading, fetchNotifications, markAsRead }
})
