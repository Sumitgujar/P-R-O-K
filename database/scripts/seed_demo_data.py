"""Idempotently seed explicitly synthetic local PROK demo data."""

import asyncio
import os
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from pymongo import AsyncMongoClient, ReturnDocument

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from indexes import INDEXES  # noqa: E402


async def upsert(db: Any, collection: str, key: str, fields: dict[str, Any]) -> dict[str, Any]:
    result = await db[collection].find_one_and_update(
        {"demo_key": key},
        {"$set": {"demo_key": key, "is_synthetic_demo_data": True, **fields}, "$setOnInsert": {"created_at": datetime.now(UTC)}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    assert result is not None
    return result


async def main() -> None:
    client = AsyncMongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"), serverSelectionTimeoutMS=5000)
    try:
        db = client[os.getenv("MONGODB_DATABASE", "prok")]
        for collection, definitions in INDEXES.items():
            for keys, options in definitions:
                await db[collection].create_index(keys, **options)

        stamp, term = datetime.now(UTC), "DEMO-2026-FALL"
        admin_user = await upsert(db, "users", "admin-user", {"email": "admin.demo@prok.example", "display_name": "Avery Admin", "role": "admin", "active": True, "updated_at": stamp})
        teacher_user = await upsert(db, "users", "teacher-user", {"email": "teacher.demo@prok.example", "display_name": "Taylor Teacher", "role": "teacher", "active": True, "updated_at": stamp})
        student_user_1 = await upsert(db, "users", "student-user-1", {"email": "student.one@prok.example", "display_name": "Sam Student", "role": "student", "active": True, "updated_at": stamp})
        student_user_2 = await upsert(db, "users", "student-user-2", {"email": "student.two@prok.example", "display_name": "Riley Student", "role": "student", "active": True, "updated_at": stamp})
        await upsert(db, "admins", "admin-profile", {"user_id": admin_user["_id"], "department": "Student Success", "permissions": ["review_documents", "view_analytics"], "updated_at": stamp})
        teacher = await upsert(db, "teachers", "teacher-profile", {"user_id": teacher_user["_id"], "employee_number": "DEMO-T-001", "department": "Computer Science", "title": "Lecturer", "updated_at": stamp})
        student_1 = await upsert(db, "students", "student-profile-1", {"user_id": student_user_1["_id"], "student_number": "DEMO-S-001", "program": {"code": "BSC-CS", "name": "BSc Computer Science"}, "year_level": 2, "academic_status": "active", "interests": ["data", "design"], "updated_at": stamp})
        student_2 = await upsert(db, "students", "student-profile-2", {"user_id": student_user_2["_id"], "student_number": "DEMO-S-002", "program": {"code": "BSC-CS", "name": "BSc Computer Science"}, "year_level": 2, "academic_status": "active", "interests": ["web", "security"], "updated_at": stamp})
        algorithms = await upsert(db, "courses", "course-algorithms", {"code": "DEMO-CS201", "title": "Algorithms Foundations", "department": "Computer Science", "credits": 4, "teacher_ids": [teacher["_id"]], "prerequisites": [], "tags": ["algorithms", "problem-solving"], "active": True, "updated_at": stamp})
        data = await upsert(db, "courses", "course-data", {"code": "DEMO-DS110", "title": "Data Literacy", "department": "Data Studies", "credits": 3, "teacher_ids": [teacher["_id"]], "prerequisites": [], "tags": ["data", "visualization"], "active": True, "updated_at": stamp})
        for student in (student_1, student_2):
            for course in (algorithms, data):
                await upsert(db, "enrollments", f"{student['demo_key']}-{course['demo_key']}", {"student_id": student["_id"], "course_id": course["_id"], "term": term, "status": "enrolled", "enrolled_at": stamp})
        session_1 = await upsert(db, "attendance_sessions", "algorithms-session-1", {"course_id": algorithms["_id"], "teacher_id": teacher["_id"], "term": term, "session_date": datetime(2026, 8, 25, tzinfo=UTC), "topic": "Algorithm analysis", "status": "closed"})
        session_2 = await upsert(db, "attendance_sessions", "algorithms-session-2", {"course_id": algorithms["_id"], "teacher_id": teacher["_id"], "term": term, "session_date": datetime(2026, 8, 27, tzinfo=UTC), "topic": "Asymptotic notation", "status": "closed"})
        for session, states in ((session_1, ("present", "present")), (session_2, ("present", "absent"))):
            for student, status in zip((student_1, student_2), states, strict=True):
                await upsert(db, "attendance_records", f"{session['demo_key']}-{student['demo_key']}", {"session_id": session["_id"], "student_id": student["_id"], "course_id": algorithms["_id"], "session_date": session["session_date"], "status": status, "recorded_by": teacher["_id"], "recorded_at": stamp})
        transcript = await upsert(db, "documents", "document-transcript", {"student_id": student_1["_id"], "document_type": "transcript", "filename": "synthetic-transcript.pdf", "storage_reference": "local://prok-demo/synthetic-transcript.pdf", "content_type": "application/pdf", "size_bytes": 124000, "status": "verified", "uploaded_at": stamp - timedelta(days=3), "verified_at": stamp - timedelta(days=2), "verified_by": admin_user["_id"]})
        await upsert(db, "documents", "document-income", {"student_id": student_1["_id"], "document_type": "income_evidence", "filename": "synthetic-income-proof.pdf", "storage_reference": "local://prok-demo/synthetic-income-proof.pdf", "content_type": "application/pdf", "size_bytes": 98000, "status": "rejected", "uploaded_at": stamp - timedelta(days=1), "verified_at": stamp, "verified_by": admin_user["_id"], "rejection_reason": "Synthetic demo document requires replacement."})
        scholarship = await upsert(db, "scholarships", "scholarship-success", {"name": "Synthetic Student Success Grant", "description": "Demo-only scholarship listing.", "eligibility_criteria": {"minimum_year_level": 2, "program_codes": ["BSC-CS"], "minimum_gpa": 3.0}, "deadline": datetime(2026, 10, 15, tzinfo=UTC), "required_documents": ["transcript", "income_evidence"], "application_information": {"instructions": "Demo only — do not submit.", "external_url": "https://example.invalid/prok-demo"}, "tags": ["need-based", "computer-science"], "status": "published", "updated_at": stamp})
        await upsert(db, "scholarship_applications", "application-success", {"student_id": student_1["_id"], "scholarship_id": scholarship["_id"], "document_ids": [transcript["_id"]], "status": "draft", "checklist": [{"document_type": "transcript", "complete": True}, {"document_type": "income_evidence", "complete": False}], "updated_at": stamp})
        await upsert(db, "recommendations", "recommendation-data", {"student_id": student_1["_id"], "type": "course", "title": "Explore Data Literacy", "explanation": "Matches declared data interest; no prerequisites.", "priority": 2, "source": {"kind": "deterministic_rule", "rule": "interest_tag_match"}, "status": "active", "created_at": stamp})
        await upsert(db, "interventions", "intervention-attendance", {"student_id": student_2["_id"], "type": "attendance_support", "reason": "Synthetic demo attendance follow-up.", "status": "open", "owner_id": teacher["_id"], "created_at": stamp, "notes": []})
        await upsert(db, "notifications", "notification-welcome", {"user_id": student_user_1["_id"], "type": "system", "title": "Welcome to the PROK demo", "body": "This is synthetic demonstration data.", "read_at": None, "created_at": stamp, "expires_at": stamp + timedelta(days=30)})
        await upsert(db, "ai_conversations", "conversation-guidance", {"student_id": student_1["_id"], "title": "Scholarship preparation", "messages": [{"role": "user", "content": "Which document is missing?", "created_at": stamp}, {"role": "assistant", "content": "Income evidence is incomplete in this demo; confirm with an administrator.", "created_at": stamp}], "message_count": 2, "updated_at": stamp, "expires_at": stamp + timedelta(days=90)})
        print(f"Seeded synthetic PROK demo data in '{db.name}'.")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
