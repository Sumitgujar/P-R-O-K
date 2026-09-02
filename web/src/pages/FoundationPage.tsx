import { API_BASE_URL, type CurrentUser } from '../services/api'

export function FoundationPage({ user, onLogout }: { user: CurrentUser; onLogout: () => void }) {
  return (
    <main className="foundation-shell">
      <p className="eyebrow">PROK · PROJECT FOUNDATION</p>
      <h1>Manage. Guide. Support. Grow.</h1>
      <p className="description">
        Signed in as {user.display_name}. The API confirmed your <strong>{user.role}</strong> role.
      </p>
      <section className="api-card" aria-label="API configuration">
        <span>Configured API base URL</span>
        <code>{API_BASE_URL}</code>
      </section>
      <button className="secondary-button" onClick={onLogout}>Sign out</button>
    </main>
  )
}
