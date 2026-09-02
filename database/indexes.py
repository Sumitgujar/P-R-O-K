"""Central index definitions for MongoDB collections introduced by PROK slices."""

INDEXES: dict[str, list[tuple[list[tuple[str, int]], dict[str, object]]]] = {
    "users": [([("email", 1)], {"unique": True, "name": "users_email_unique"})],
    "enrollments": [
        (
            [("student_id", 1), ("course_id", 1), ("term", 1)],
            {"unique": True, "name": "enrollments_student_course_term_unique"},
        )
    ],
    "attendance_events": [
        (
            [("student_id", 1), ("course_id", 1), ("session_date", 1)],
            {"name": "attendance_student_course_date"},
        )
    ],
}
