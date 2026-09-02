"""Repeatable MongoDB index definitions for PROK."""

IndexDefinition = tuple[list[tuple[str, int]], dict[str, object]]

INDEXES: dict[str, list[IndexDefinition]] = {
    "users": [
        ([("email", 1)], {"unique": True, "name": "users_email_unique"}),
        ([("role", 1), ("active", 1)], {"name": "users_role_active"}),
    ],
    "students": [
        ([("user_id", 1)], {"unique": True, "name": "students_user_unique"}),
        ([("student_number", 1)], {"unique": True, "name": "students_number_unique"}),
        ([("program.code", 1), ("academic_status", 1)], {"name": "students_program_status"}),
    ],
    "teachers": [
        ([("user_id", 1)], {"unique": True, "name": "teachers_user_unique"}),
        ([("employee_number", 1)], {"unique": True, "name": "teachers_number_unique"}),
    ],
    "admins": [([("user_id", 1)], {"unique": True, "name": "admins_user_unique"})],
    "courses": [
        ([("code", 1)], {"unique": True, "name": "courses_code_unique"}),
        ([("active", 1), ("department", 1)], {"name": "courses_active_department"}),
        ([("teacher_ids", 1), ("active", 1)], {"name": "courses_teacher_active"}),
    ],
    "enrollments": [
        ([("student_id", 1), ("course_id", 1), ("term", 1)], {"unique": True, "name": "enrollments_student_course_term_unique"}),
        ([("course_id", 1), ("term", 1), ("status", 1)], {"name": "enrollments_course_term"}),
    ],
    "attendance_sessions": [
        ([("course_id", 1), ("term", 1), ("session_date", -1)], {"name": "sessions_course_term_date"}),
        ([("teacher_id", 1), ("session_date", -1)], {"name": "sessions_teacher_date"}),
    ],
    "attendance_records": [
        ([("session_id", 1), ("student_id", 1)], {"unique": True, "name": "records_session_student_unique"}),
        ([("student_id", 1), ("course_id", 1), ("session_date", -1)], {"name": "records_student_course_date"}),
    ],
    "documents": [
        ([("student_id", 1), ("document_type", 1), ("uploaded_at", -1)], {"name": "documents_student_type"}),
        ([("status", 1), ("uploaded_at", 1)], {"name": "documents_review_queue"}),
        ([("storage_reference", 1)], {"unique": True, "name": "documents_storage_reference_unique"}),
    ],
    "scholarships": [
        ([("status", 1), ("deadline", 1)], {"name": "scholarships_status_deadline"}),
        ([("tags", 1), ("status", 1)], {"name": "scholarships_tags_status"}),
    ],
    "scholarship_applications": [
        ([("student_id", 1), ("scholarship_id", 1)], {"unique": True, "name": "applications_student_scholarship_unique"}),
        ([("status", 1), ("submitted_at", 1)], {"name": "applications_review_queue"}),
    ],
    "recommendations": [
        ([("student_id", 1), ("created_at", -1)], {"name": "recommendations_student_recent"}),
        ([("student_id", 1), ("status", 1), ("priority", -1)], {"name": "recommendations_student_active"}),
    ],
    "interventions": [
        ([("student_id", 1), ("status", 1), ("created_at", -1)], {"name": "interventions_student_status"}),
        ([("owner_id", 1), ("status", 1)], {"name": "interventions_owner_queue"}),
    ],
    "notifications": [
        ([("user_id", 1), ("read_at", 1), ("created_at", -1)], {"name": "notifications_user_inbox"}),
        ([("expires_at", 1)], {"expireAfterSeconds": 0, "name": "notifications_expiry"}),
    ],
    "ai_conversations": [
        ([("student_id", 1), ("updated_at", -1)], {"name": "conversations_student_recent"}),
        ([("expires_at", 1)], {"expireAfterSeconds": 0, "name": "conversations_expiry"}),
    ],
}
