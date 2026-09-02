export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1'

export type UserRole = 'student' | 'teacher' | 'admin'

export interface CurrentUser {
  id: string
  email: string
  display_name: string
  role: UserRole
}

interface TokenResponse {
  access_token: string
  token_type: 'bearer'
  expires_in: number
}

export class ApiError extends Error {
  constructor(message: string, readonly status: number) {
    super(message)
  }
}

async function request<T>(path: string, options: RequestInit = {}, token?: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}), ...options.headers },
  })
  if (!response.ok) {
    const data = await response.json().catch(() => ({})) as { detail?: string }
    throw new ApiError(data.detail ?? 'Request failed', response.status)
  }
  return response.json() as Promise<T>
}

export const authApi = {
  login(email: string, password: string) {
    return request<TokenResponse>('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) })
  },
  currentUser(token: string) {
    return request<CurrentUser>('/auth/me', {}, token)
  },
  logout(token: string) {
    return request('/auth/logout', { method: 'POST' }, token)
  },
}
