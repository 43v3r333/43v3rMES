import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'
import type { User } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const sessionRestored = ref(false)
  const isRestoring = ref(false)
  const hasTriedRestore = ref(false)
  const restoreFailed = ref(false)

  const isAuthenticated = computed(() => !!accessToken.value)

  function loadTokensFromStorage() {
    const storedAccess = localStorage.getItem('access_token')
    const storedRefresh = localStorage.getItem('refresh_token')
    
    if (storedAccess) {
      accessToken.value = storedAccess
    }
    
    if (storedRefresh) {
      refreshToken.value = storedRefresh
    }
  }

  async function login(credentials: URLSearchParams) {
    const { data } = await api.post('/auth/login', credentials, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })

    accessToken.value = data.access_token
    refreshToken.value = data.refresh_token
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('refresh_token', data.refresh_token)

    await fetchUserProfile()
  }

  async function fetchUserProfile() {
    try {
      const { data } = await api.get('/auth/me')
      user.value = data
    } catch (e) {
      throw e
    }
  }

  async function logout() {
    if (refreshToken.value) {
      try {
        await api.post('/auth/logout', { refresh_token: refreshToken.value })
      } catch (e) {
        // Continue logout anyway
      }
    }
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    sessionRestored.value = false
    isRestoring.value = false
    hasTriedRestore.value = false
    restoreFailed.value = false
  }

  async function restoreSession() {
    if (isRestoring.value) {
      return
    }
    
    isRestoring.value = true
    hasTriedRestore.value = true
    
    try {
      loadTokensFromStorage()
      
      if (accessToken.value) {
        try {
          await fetchUserProfile()
          sessionRestored.value = true
          restoreFailed.value = false
        } catch (e) {
          console.error('Session restoration failed:', e)
          logout()
          sessionRestored.value = true
          restoreFailed.value = true
        }
      } else {
        sessionRestored.value = true
        restoreFailed.value = false
      }
    } finally {
      isRestoring.value = false
    }
  }

  function validateSession() {
    loadTokensFromStorage()
    return !!accessToken.value
  }

  function clearSession() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    sessionRestored.value = false
    hasTriedRestore.value = false
    restoreFailed.value = false
  }

  return {
    user,
    accessToken,
    refreshToken,
    isAuthenticated,
    sessionRestored,
    isRestoring,
    hasTriedRestore,
    restoreFailed,
    login,
    logout,
    fetchUserProfile,
    restoreSession,
    validateSession,
    clearSession
  }
})
