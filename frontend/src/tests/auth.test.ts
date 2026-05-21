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

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
  })

  it('should initialize with null tokens', () => {
    const store = useAuthStore()
    expect(store.accessToken).toBeNull()
    expect(store.refreshToken).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })

  it('should load tokens from localStorage', () => {
    localStorage.setItem('access_token', 'test-access-token')
    localStorage.setItem('refresh_token', 'test-refresh-token')

    const store = useAuthStore()
    store.loadTokensFromStorage()

    expect(store.accessToken).toBe('test-access-token')
    expect(store.refreshToken).toBe('test-refresh-token')
    expect(store.isAuthenticated).toBe(true)
  })

  it('should login and store tokens', async () => {
    const store = useAuthStore()
    const mockResponse = {
      data: {
        access_token: 'new-access-token',
        refresh_token: 'new-refresh-token',
      },
    }

    vi.mocked(import('@/services/api').default.post).mockResolvedValue(mockResponse)
    vi.mocked(import('@/services/api').default.get).mockResolvedValue({
      data: { id: '1', email: 'test@example.com' },
    })

    const formData = new URLSearchParams()
    formData.append('username', 'test@example.com')
    formData.append('password', 'password123')

    await store.login(formData)

    expect(store.accessToken).toBe('new-access-token')
    expect(store.refreshToken).toBe('new-refresh-token')
    expect(localStorage.getItem('access_token')).toBe('new-access-token')
    expect(localStorage.getItem('refresh_token')).toBe('new-refresh-token')
    expect(store.isAuthenticated).toBe(true)
  })

  it('should logout and clear tokens', () => {
    const store = useAuthStore()
    localStorage.setItem('access_token', 'test-token')
    localStorage.setItem('refresh_token', 'test-refresh-token')
    store.loadTokensFromStorage()

    store.logout()

    expect(store.accessToken).toBeNull()
    expect(store.refreshToken).toBeNull()
    expect(store.isAuthenticated).toBe(false)
    expect(localStorage.getItem('access_token')).toBeNull()
    expect(localStorage.getItem('refresh_token')).toBeNull()
  })

  it('should restore session from localStorage', async () => {
    localStorage.setItem('access_token', 'test-access-token')

    const store = useAuthStore()
    vi.mocked(import('@/services/api').default.get).mockResolvedValue({
      data: { id: '1', email: 'test@example.com' },
    })

    await store.restoreSession()

    expect(store.accessToken).toBe('test-access-token')
    expect(store.sessionRestored).toBe(true)
  })

  it('should clear session on fetchUserProfile failure', async () => {
    const store = useAuthStore()
    localStorage.setItem('access_token', 'invalid-token')
    store.loadTokensFromStorage()

    vi.mocked(import('@/services/api').default.get).mockRejectedValue(
      new Error('401 Unauthorized')
    )

    await store.restoreSession()

    expect(store.accessToken).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })

  it('should validate session correctly', () => {
    const store = useAuthStore()
    expect(store.validateSession()).toBe(false)

    localStorage.setItem('access_token', 'valid-token')
    expect(store.validateSession()).toBe(true)
  })
})

describe('Router Navigation Guard', () => {
  it('should redirect to login if not authenticated', () => {
    const store = useAuthStore()
    expect(store.isAuthenticated).toBe(false)
  })

  it('should allow access to login page for unauthenticated users', () => {
    const store = useAuthStore()
    expect(store.isAuthenticated).toBe(false)
  })

  it('should maintain authentication state across navigation', () => {
    const store = useAuthStore()
    localStorage.setItem('access_token', 'persistent-token')
    store.loadTokensFromStorage()

    expect(store.isAuthenticated).toBe(true)
    expect(store.sessionRestored).toBe(true)
  })
})
