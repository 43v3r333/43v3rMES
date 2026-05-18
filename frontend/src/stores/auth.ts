import { defineStore } from 'pinia'; import { ref, computed } from 'vue'
export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token')); const isAuthenticated = computed(() => !!token.value)
  async function login(credentials: any) { token.value = 'fake-token'; localStorage.setItem('token', token.value) }
  function logout() { token.value = null; localStorage.removeItem('token') }
  return { token, isAuthenticated, login, logout }
})
