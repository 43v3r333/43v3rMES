<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseButton from '@/components/ui/BaseButton.vue'

const authStore = useAuthStore()
const router = useRouter()

const email = ref('')
const password = ref('')
const error = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
  error.value = ''
  isLoading.value = true
  try {
    const formData = new URLSearchParams()
    formData.append('username', email.value)
    formData.append('password', password.value)

    await authStore.login(formData)
    router.push('/')
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Authentication failed. Please check your credentials.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-muted/30 px-4">
    <div class="max-w-md w-full space-y-8 p-8 bg-card border rounded shadow-lg">
      <div class="text-center">
        <h1 class="text-3xl font-extrabold tracking-tight text-primary">43v3rMES</h1>
        <p class="mt-2 text-sm text-muted-foreground uppercase tracking-widest font-semibold">Enterprise Operations</p>
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="space-y-4">
          <div class="space-y-1">
            <label for="email" class="text-xs font-bold uppercase text-muted-foreground">User Email</label>
            <input
              v-model="email"
              id="email"
              type="email"
              required
              class="block w-full px-3 py-2 border rounded-md shadow-sm focus:ring-primary focus:border-primary text-sm bg-background transition-all"
              placeholder="admin@factory.com"
            />
          </div>
          <div class="space-y-1">
            <label for="password" class="text-xs font-bold uppercase text-muted-foreground">Security Password</label>
            <input
              v-model="password"
              id="password"
              type="password"
              required
              class="block w-full px-3 py-2 border rounded-md shadow-sm focus:ring-primary focus:border-primary text-sm bg-background transition-all"
              placeholder="••••••••"
            />
          </div>
        </div>

        <div v-if="error" class="p-3 rounded bg-destructive/10 border border-destructive/20 text-destructive text-xs font-bold text-center">
          {{ error }}
        </div>

        <BaseButton
          type="submit"
          class="w-full h-11"
          :loading="isLoading"
        >
          Sign In to System
        </BaseButton>
      </form>

      <div class="mt-6 pt-6 border-t text-center">
        <p class="text-[10px] text-muted-foreground uppercase tracking-tighter">
          Authorized personnel only. All access is logged and monitored.
        </p>
      </div>
    </div>
  </div>
</template>
