<script setup lang="ts">import { ref } from 'vue'; import { useRouter } from 'vue-router'; import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore(); const router = useRouter(); const email = ref(''); const password = ref('')
const handleLogin = async () => { await authStore.login({}); router.push('/') }
</script>
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="max-w-md w-full p-8 bg-white shadow-md rounded-lg">
      <h2 class="text-2xl font-bold text-center mb-6">AI MES Login</h2>
      <form @submit.prevent="handleLogin" class="space-y-4">
        <input v-model="email" type="email" placeholder="Email" class="w-full p-2 border rounded" required />
        <input v-model="password" type="password" placeholder="Password" class="w-full p-2 border rounded" required />
        <button type="submit" class="w-full bg-blue-600 text-white p-2 rounded">Sign In</button>
      </form>
    </div>
  </div>
</template>
