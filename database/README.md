# PROK MongoDB design

PROK uses MongoDB exclusively. Documents use `ObjectId` references for independently changing, high-cardinality entities and embed only compact values needed together.

## Initialize local development data

```powershell
docker compose up -d mongodb
backend\.venv\Scripts\python database/scripts/create_indexes.py
backend\.venv\Scripts\python database/scripts/seed_demo_data.py
backend\.venv\Scripts\python database/scripts/verify_backend_crud.py
```

The seeder is idempotent and only writes records carrying `is_synthetic_demo_data: true`. It represents no real institution, people, scholarship, or policy.

## Collections

| Collection | Design and usage |
| --- | --- |
| `users` | Identity root: email, display name, role, active state. |
| `students` | Unique `user_id`; student number, program subdocument, year, status, interests. |
| `teachers` | Unique `user_id`; employee number, department, title. |
| `admins` | Unique `user_id`; department and compact permissions. |
| `courses` | Catalog document: code, credits, tags, prerequisites, small `teacher_ids` array. |
| `enrollments` | Student/course/term relationship and status; kept separate for history and rosters. |
| `attendance_sessions` | Teacher-created course meeting with term, date, topic, status. |
| `attendance_records` | One student/session record; references session and denormalizes course/date for dashboard reads. |
| `documents` | Student file metadata and verification workflow; no file binary. |
| `scholarships` | Published opportunity with embedded criteria, document requirements, deadline, instructions. |
| `scholarship_applications` | Student/scholarship state, linked document IDs, checklist snapshot. |
| `recommendations` | Student-targeted type, explanation, priority, source/rule evidence and status. |
| `interventions` | Human-owned student-support workflow: reason, owner, status, compact notes. |
| `notifications` | Per-user inbox; `expires_at` TTL index cleans old notifications. |
| `ai_conversations` | Minimal metadata and bounded messages; no copied profile/document data; TTL expiry. |

## Storage abstraction

`documents.storage_reference` is an opaque storage key, for example `local://...` in development or a cloud object key later. A future storage service resolves it after authorization. MongoDB stores metadata, status, and audit fields including `verified_at`, `verified_by`, and optional `rejection_reason`.

## Indexes and CRUD verification

`indexes.py` contains the repeatable index definitions: unique identity/profile/course/enrollment/attendance/application keys; dashboard, roster, review-queue and inbox query indexes; and TTL indexes for notifications and AI conversations.

`verify_backend_crud.py` imports the backend `MongoRepository`, then creates, reads, updates, deletes, and confirms deletion of a temporary notification. It leaves no record behind; run it only against a development database.

The same check is available as an optional Python integration test:

```powershell
$env:RUN_MONGO_INTEGRATION=1
backend\.venv\Scripts\python -m unittest discover -s backend/tests -p test_mongodb_crud.py
```
