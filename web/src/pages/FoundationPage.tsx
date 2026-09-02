import { API_BASE_URL } from '../services/api'

export function FoundationPage() {
  return (
    <main className="foundation-shell">
      <p className="eyebrow">PROK · PROJECT FOUNDATION</p>
      <h1>Manage. Guide. Support. Grow.</h1>
      <p className="description">
        The PROK web dashboard foundation is ready for the future student, teacher, and admin experiences.
      </p>
      <section className="api-card" aria-label="API configuration">
        <span>Configured API base URL</span>
        <code>{API_BASE_URL}</code>
      </section>
    </main>
  )
}
