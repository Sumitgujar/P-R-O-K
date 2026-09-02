# PROK MVP implementation plan

## 1. Goal and scope

PROK is a cross-platform College Personal Guide with three roles:

- **Student:** view attendance insight, manage personal documents, receive scholarship preparation guidance, explore course suggestions, and use a college guide.
- **Teacher:** manage class attendance records for assigned classes and view simple class-level summaries.
- **Admin:** manage reference data and review workflow items that need institutional authority.

The first usable demo should prove one coherent student journey, not every listed feature:

1. A student signs in to a demo account.
2. The student sees attendance calculated from stored records and a clear attendance-risk explanation.
3. The student uploads or registers a document and sees its preparation/checklist status.
4. The student receives deterministic course suggestions based on declared interests and completed courses.
5. The guide answers only from supplied, approved demo knowledge and clearly distinguishes guidance from official decisions.

Teacher attendance entry and a small admin reference-data view are included only after that journey works end to end.

## 2. Architecture

```text
Flutter (Android/mobile) ─┐
                           ├─ HTTPS/JSON ─ FastAPI ─ MongoDB
React/Vite dashboard ─────┘                    │
                                                ├─ rule-based services
                                                └─ optional AI adapter
```

### Client responsibilities

- **Flutter / Dart:** student-first mobile experience; responsive layouts; typed API client; secure local token storage when authentication is introduced.
- **React + Vite + TypeScript:** teacher/admin desktop dashboard and a responsive student fallback; typed API client and role-aware routes.

### Backend responsibilities

- **FastAPI + Pydantic:** versioned REST API, validation, authentication/authorization middleware, OpenAPI documentation, and centralized error responses.
- **MongoDB:** source of truth for users, attendance events, documents, course catalog, recommendation inputs, workflow states, and curated guide knowledge.
- **Async driver:** start with the current official asynchronous MongoDB Python driver appropriate at implementation time; isolate it behind repository interfaces so a driver change does not affect route or business logic.

### Service boundaries

- `attendance_service`: computes totals, percentages, required future attendance, and risk labels from stored attendance events and configured rules.
- `document_service`: tracks metadata, owner, status, and checklist; files should be stored in an object store or local development storage rather than MongoDB documents.
- `scholarship_service`: matches a student against explicitly stored criteria and reports missing evidence; it does not decide eligibility.
- `recommendation_service`: begins with transparent rules such as interests, completed courses, prerequisites, and availability.
- `guide_service`: retrieves approved knowledge and optionally asks an LLM to phrase an answer. It must cite/identify its source context, refuse unknown facts, and never mutate institutional data.

No API route should call an LLM directly. Routes call a service interface; an AI adapter is optional and replaceable.

## 3. Initial backend layout

```text
backend/
├── app/
│   ├── api/v1/              # routers grouped by capability
│   ├── core/                # config, security, logging, dependencies
│   ├── db/                  # Mongo client, indexes, repository interfaces
│   ├── models/              # Pydantic request/response models
│   ├── repositories/        # Mongo persistence implementations
│   ├── services/            # deterministic business logic + AI ports
│   └── main.py
├── tests/
└── pyproject.toml
```

Keep database documents private to repositories. API responses use explicit Pydantic schemas; never return raw MongoDB documents or expose internal fields.

## 4. MongoDB collections (MVP direction)

| Collection | Purpose | Important fields |
| --- | --- | --- |
| `users` | accounts and role identity | `_id`, `email`, `role`, `profile`, `active` |
| `courses` | approved course catalog | `_id`, `code`, `title`, `credits`, `prerequisites`, `tags`, `active` |
| `enrollments` | student/course membership | `student_id`, `course_id`, `term`, `status` |
| `attendance_events` | teacher-recorded attendance | `student_id`, `course_id`, `session_date`, `status`, `recorded_by` |
| `documents` | file metadata and workflow | `owner_id`, `type`, `storage_key`, `status`, `checklist` |
| `scholarships` | curated opportunity criteria | `title`, `criteria`, `required_documents`, `status` |
| `recommendation_profiles` | declared student preferences | `student_id`, `interests`, `goals`, `updated_at` |
| `guide_knowledge` | approved guide content | `title`, `body`, `audience`, `source_label`, `published` |
| `audit_events` | material human actions | `actor_id`, `action`, `entity_type`, `entity_id`, `created_at` |

Required indexes will be added with the relevant repository implementation, beginning with unique `users.email`, unique enrollment per student/course/term, and attendance lookup by student/course/date.

## 5. API direction

Use `/api/v1` and standard JSON response envelopes only where they add value; ordinary resource responses should remain simple.

- `POST /auth/login` and `GET /auth/me`
- `GET /students/me/dashboard`
- `GET /students/me/attendance` and `GET /students/me/attendance/{course_id}`
- `POST /teacher/attendance` for authorized teachers
- `GET/POST /documents` and `PATCH /documents/{id}`
- `GET /scholarships` and `GET /scholarships/{id}/checklist`
- `GET /recommendations/courses`
- `POST /guide/questions`

Every write must authenticate the actor, authorize their role and ownership/assignment, validate input, and emit an audit event when it changes an important record.

## 6. Safety, privacy, and responsible AI

- Use synthetic, clearly marked demo data only.
- Store passwords only as strong hashes; never log credentials, tokens, document contents, or personally identifying data unnecessarily.
- Enforce role and resource-level authorization server-side; hiding a client button is not authorization.
- Validate file type and size, generate non-guessable storage keys, and authorize every download.
- Make attendance formulas and recommendation reasons visible to students.
- Label AI output as guidance; link it to approved knowledge where applicable and state when official confirmation is needed.
- Never allow AI to record attendance, approve a scholarship, alter documents, or change a course enrollment.

## 7. Delivery phases

### Phase 0 — foundation

Create the three application shells, environment configuration, lint/format/test commands, API health endpoint, MongoDB local setup, and a minimal seed mechanism for explicitly synthetic demo data.

### Phase 1 — student attendance slice

Implement authenticated demo roles, course enrollment, attendance entry by a teacher, and student attendance dashboard with deterministic calculations and explanations.

### Phase 2 — documents and scholarship checklist

Add document metadata/upload workflow, curated scholarship records, and a missing-document checklist. Keep approval states human-controlled.

### Phase 3 — transparent recommendations and guide

Add profile preferences, explainable rule-based course recommendations, curated knowledge retrieval, and an optional AI phrasing adapter.

### Phase 4 — dashboard polish and demo readiness

Add teacher/admin dashboard views, empty/loading/error states, accessibility pass, responsive verification, API documentation, and a scripted demo flow.

## 8. Development rules

- Prefer one vertical slice at a time, complete with API validation and a client view.
- Add tests for attendance calculations, authorization boundaries, recommendation reasons, and guide grounding rules before broad UI polish.
- Keep secrets in ignored local environment files; commit an `.env.example` without values.
- Use TypeScript strict mode and Dart analysis; format Python, TypeScript, and Dart in CI/local checks.
- Add dependencies only when a concrete MVP slice needs them.
- Keep all AI provider configuration optional. The application must function without an LLM key.
- Do not introduce microservices, queues, vector databases, realtime sync, or institutional integrations unless a demonstrated MVP need emerges.

## 9. Decisions still needed before implementation

1. Authentication approach for the demo: local seeded accounts versus a chosen identity provider.
2. File storage choice for the demo: local development storage versus a selected cloud object store.
3. Source and approval owner for university guide knowledge and scholarship criteria.
4. The institution's attendance policy rules (threshold, excused attendance treatment, and term/course scope).
5. Which single student journey is most important for hackathon judging.

Until those inputs are available, Phase 0 can use configurable placeholder policies and clearly synthetic seed data, never institution-specific claims.
