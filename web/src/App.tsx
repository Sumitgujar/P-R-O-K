import { useEffect, useState } from 'react'

import { AuthPage } from './pages/AuthPage'
import { FoundationPage } from './pages/FoundationPage'
import { authApi, type CurrentUser } from './services/api'

export function App() {
  const [token, setToken] = useState(() => sessionStorage.getItem('prok_access_token'))
  const [user, setUser] = useState<CurrentUser>()

  useEffect(() => {
    if (!token) return
    authApi.currentUser(token).then(setUser).catch(() => {
      sessionStorage.removeItem('prok_access_token')
      setToken(null)
    })
  }, [token])

  if (!token || !user) {
    return <AuthPage onAuthenticated={(nextToken, nextUser) => {
      sessionStorage.setItem('prok_access_token', nextToken)
      setToken(nextToken)
      setUser(nextUser)
    }} />
  }
  return <FoundationPage user={user} onLogout={async () => {
    await authApi.logout(token).catch(() => undefined)
    sessionStorage.removeItem('prok_access_token')
    setToken(null)
    setUser(undefined)
  }} />
}
