import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import { describe, it, expect, beforeEach, vi } from 'vitest'

vi.mock('@/services/api', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn(),
  },
}))

describe('Edge Cases - Session Management', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
  })

  it('should handle page refresh with valid token', async () => {
    const testToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzAwMDAwMDAwfQ.test'
    localStorage.setItem('access_token', testToken)

    const store = useAuthStore()
    vi.mocked(import('@/services/api').default.get).mockResolvedValue({
      data: { id: '1', email: 'test@example.com' },
    })

    await store.restoreSession()

    expect(store.accessToken).toBe(testToken)
    expect(store.sessionRestored).toBe(true)
    expect(store.isAuthenticated).toBe(true)
  })

  it('should handle tab switching with shared localStorage', async () => {
    const store1 = useAuthStore()
    const store2 = useAuthStore()

    localStorage.setItem('access_token', 'shared-token')
    localStorage.setItem('refresh_token', 'shared-refresh')

    store1.loadTokensFromStorage()
    store2.loadTokensFromStorage()

    expect(store1.accessToken).toBe('shared-token')
    expect(store2.accessToken).toBe('shared-token')
    expect(store1.isAuthenticated).toBe(true)
    expect(store2.isAuthenticated).toBe(true)
  })

  it('should handle extended session duration', async () => {
    const store = useAuthStore()
    localStorage.setItem('access_token', 'long-session-token')
    localStorage.setItem('refresh_token', 'long-refresh-token')

    store.loadTokensFromStorage()

    expect(store.accessToken).toBe('long-session-token')
    expect(store.refreshToken).toBe('long-refresh-token')
    expect(store.isAuthenticated).toBe(true)

    await store.restoreSession()

    expect(store.sessionRestored).toBe(true)
  })

  it('should clear session on token invalidation', async () => {
    const store = useAuthStore()
    localStorage.setItem('access_token', 'invalidated-token')
    localStorage.setItem('refresh_token', 'invalidated-refresh')

    store.loadTokensFromStorage()
    expect(store.isAuthenticated).toBe(true)

    vi.mocked(import('@/services/api').default.get).mockRejectedValue(
      new Error('401 Unauthorized')
    )

    await store.restoreSession()

    expect(store.accessToken).toBeNull()
    expect(store.refreshToken).toBeNull()
    expect(store.isAuthenticated).toBe(false)
    expect(localStorage.getItem('access_token')).toBeNull()
  })

  it('should handle missing refresh token during 401', async () => {
    localStorage.removeItem('refresh_token')

    const store = useAuthStore()
    store.loadTokensFromStorage()

    expect(store.refreshToken).toBeNull()
  })

  it('should maintain session state after multiple navigation events', async () => {
    const store = useAuthStore()
    localStorage.setItem('access_token', 'persistent-session-token')
    localStorage.setItem('refresh_token', 'persistent-refresh-token')

    store.loadTokensFromStorage()
    await store.restoreSession()

    expect(store.isAuthenticated).toBe(true)
    expect(store.sessionRestored).toBe(true)

    const originalAccessToken = store.accessToken

    store.loadTokensFromStorage()

    expect(store.accessToken).toBe(originalAccessToken)
    expect(store.isAuthenticated).toBe(true)
  })

  it('should handle concurrent session restoration', async () => {
    const store = useAuthStore()
    localStorage.setItem('access_token', 'concurrent-token')

    const restorationPromises = Array(5).fill(null).map(() => store.restoreSession())
    await Promise.all(restorationPromises)

    expect(store.accessToken).toBe('concurrent-token')
    expect(store.sessionRestored).toBe(true)
  })

  it('should handle token expiration during navigation', async () => {
    const store = useAuthStore()
    localStorage.setItem('access_token', 'expired-token')
    localStorage.setItem('refresh_token', 'valid-refresh-token')

    store.loadTokensFromStorage()

    vi.mocked(import('@/services/api').default.get).mockRejectedValue(
      new Error('401 Unauthorized')
    )

    await store.restoreSession()

    expect(store.accessToken).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })

  it('should handle logout from multiple tabs', async () => {
    const store1 = useAuthStore()
    const store2 = useAuthStore()

    localStorage.setItem('access_token', 'multi-tab-token')
    localStorage.setItem('refresh_token', 'multi-tab-refresh')

    store1.loadTokensFromStorage()
    store2.loadTokensFromStorage()

    expect(store1.isAuthenticated).toBe(true)
    expect(store2.isAuthenticated).toBe(true)

    store1.logout()

    expect(store1.isAuthenticated).toBe(false)
    expect(store2.isAuthenticated).toBe(true)

    store2.loadTokensFromStorage()
    expect(store2.isAuthenticated).toBe(false)
  })
})

describe('Security - Token Management', () => {
  it('should not store tokens in memory after logout', async () => {
    const store = useAuthStore()
    localStorage.setItem('access_token', 'secure-token')
    localStorage.setItem('refresh_token', 'secure-refresh')

    store.loadTokensFromStorage()
    expect(store.isAuthenticated).toBe(true)

    store.logout()

    expect(store.accessToken).toBeNull()
    expect(store.refreshToken).toBeNull()
    expect(localStorage.getItem('access_token')).toBeNull()
  })

  it('should clear sessionRestored flag on logout', () => {
    const store = useAuthStore()
    localStorage.setItem('access_token', 'test-token')
    store.loadTokensFromStorage()
    store.restoreSession()

    store.logout()

    expect(store.sessionRestored).toBe(false)
  })
})
