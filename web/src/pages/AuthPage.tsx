import { FormEvent, useState } from 'react'

import { ApiError, API_BASE_URL, authApi, type CurrentUser } from '../services/api'

interface Props {
  onAuthenticated: (token: string, user: CurrentUser) => void
}

export function AuthPage({ onAuthenticated }: Props) {
  const [email, setEmail] = useState('student.one@prok.example')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string>()
  const [submitting, setSubmitting] = useState(false)

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSubmitting(true)
    setError(undefined)
    try {
      const token = await authApi.login(email, password)
      const user = await authApi.currentUser(token.access_token)
      onAuthenticated(token.access_token, user)
    } catch (cause) {
      setError(cause instanceof ApiError ? cause.message : 'Unable to reach the PROK API.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="foundation-shell">
      <p className="eyebrow">PROK · SECURE SIGN IN</p>
      <h1>Welcome back.</h1>
      <p className="description">Sign in with a PROK account. Your role is determined by the API, never by this form.</p>
      <form className="api-card auth-form" onSubmit={submit}>
        <label>Email<input type="email" value={email} onChange={(event) => setEmail(event.target.value)} required /></label>
        <label>Password<input type="password" value={password} onChange={(event) => setPassword(event.target.value)} required /></label>
        {error && <p className="form-error" role="alert">{error}</p>}
        <button type="submit" disabled={submitting}>{submitting ? 'Signing in…' : 'Sign in'}</button>
      </form>
      <p className="api-hint">API: <code>{API_BASE_URL}</code></p>
    </main>
  )
}
