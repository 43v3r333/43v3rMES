<script setup lang="ts">
import { ref } from 'vue'
import { RouterView, useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useDarkMode } from '@/composables/useDarkMode'
import { useNotificationStore } from '@/stores/notification'
import NotificationPanel from '@/components/ui/NotificationPanel.vue'
import {
  Radio,
  Activity,
  AlertCircle,
  Clock,
  Users,
  Maximize2,
  RefreshCcw,
  LayoutDashboard,
  Settings,
  LogOut,
  Factory,
  ShieldAlert,
  Bell,
  ChevronRight,
  Menu,
  X,
  Sun,
  Moon,
  Wrench,
  Calendar
} from 'lucide-vue-next'

const authStore = useAuthStore()
const notificationStore = useNotificationStore()
const router = useRouter()
const route = useRoute()
const { isDark, toggleDark } = useDarkMode()

const isSidebarOpen = ref(true)
const isNotificationsOpen = ref(false)

const navigation = [
  { name: 'Command Center', href: '/', icon: Radio },
  { name: 'Machines', href: '/machines', icon: Factory },
  { name: 'Downtime', href: '/downtime', icon: Activity },
  { name: 'Work Orders', href: '/maintenance', icon: Wrench },
  { name: 'PM Plans', href: '/maintenance/schedules', icon: Calendar },
  { name: 'Analytics', href: '/analytics', icon: LayoutDashboard },
  { name: 'Handovers', href: '/handovers', icon: Users },
  { name: 'Escalations', href: '/escalations', icon: ShieldAlert },
  { name: 'Settings', href: '/settings', icon: Settings },
]

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen bg-background flex text-foreground font-sans">
    <!-- Sidebar -->
    <aside
      :class="[
        'bg-card border-r w-64 flex-shrink-0 transition-all duration-300 ease-in-out flex flex-col',
        isSidebarOpen ? 'ml-0' : '-ml-64'
      ]"
    >
      <div class="h-16 flex items-center px-6 border-b shrink-0">
        <span class="text-xl font-black tracking-tighter text-primary">43v3rMES</span>
      </div>
      <nav class="flex-1 p-4 space-y-1 overflow-y-auto">
        <router-link
          v-for="item in navigation"
          :key="item.name"
          :to="item.href"
          class="flex items-center px-3 py-2 text-sm font-semibold rounded-md hover:bg-accent hover:text-accent-foreground transition-colors"
          active-class="bg-accent text-accent-foreground"
        >
          <component :is="item.icon" class="mr-3 h-4 w-4" />
          {{ item.name }}
        </router-link>
      </nav>
      <div class="p-4 border-t shrink-0">
        <button
          @click="handleLogout"
          class="flex w-full items-center px-3 py-2 text-sm font-bold text-destructive rounded-md hover:bg-destructive/10 transition-colors uppercase tracking-tighter"
        >
          <LogOut class="mr-3 h-4 w-4" />
          Terminate Session
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden relative">
      <header class="h-16 bg-card border-b flex items-center justify-between px-6 shrink-0">
        <div class="flex items-center">
          <button @click="isSidebarOpen = !isSidebarOpen" class="p-2 -ml-2 rounded-md hover:bg-accent">
            <Menu v-if="!isSidebarOpen" class="h-5 w-5" />
            <X v-else class="h-5 w-5" />
          </button>

          <nav class="ml-4 flex items-center space-x-2 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">
            <span>Enterprise</span>
            <ChevronRight class="h-3 w-3" />
            <span class="text-foreground">{{ route.name }}</span>
          </nav>
        </div>

        <div class="flex items-center space-x-3">
          <!-- Notification Bell -->
          <div class="relative">
            <button @click="isNotificationsOpen = !isNotificationsOpen" class="p-2 rounded-md hover:bg-accent relative">
              <Bell class="h-5 w-5" />
              <span v-if="notificationStore.unreadCount > 0" class="absolute top-1 right-1 h-2 w-2 bg-primary rounded-full"></span>
            </button>
            <div v-if="isNotificationsOpen" class="absolute right-0 mt-2 z-50">
              <NotificationPanel />
            </div>
          </div>

          <button @click="toggleDark" class="p-2 rounded-md hover:bg-accent transition-colors">
            <Sun v-if="isDark" class="h-5 w-5" />
            <Moon v-else class="h-5 w-5" />
          </button>
          <div class="h-8 w-px bg-border"></div>
          <div class="flex items-center space-x-3">
            <div class="text-right hidden sm:block">
              <div class="text-xs font-black uppercase tracking-tighter">Enterprise Admin</div>
              <div class="text-[10px] text-muted-foreground font-bold uppercase">Main Factory</div>
            </div>
            <div class="h-8 w-8 rounded bg-primary flex items-center justify-center text-primary-foreground font-black text-xs">
              EA
            </div>
          </div>
        </div>
      </header>
      <main class="flex-1 overflow-y-auto p-6 bg-muted/20" @click="isNotificationsOpen = false">
        <div class="max-w-7xl mx-auto">
          <RouterView />
        </div>
      </main>
    </div>
  </div>
</template>
