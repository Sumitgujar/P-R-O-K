import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

from bson import ObjectId

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.core.dependencies import get_database
from app.core.security import hash_password
from app.main import app


class FakeCollection:
    def __init__(self) -> None:
        self.documents: list[dict] = []

    @staticmethod
    def matches(document: dict, query: dict) -> bool:
        return all(document.get(key) == value for key, value in query.items())

    async def find_one(self, query: dict) -> dict | None:
        return next((document for document in self.documents if self.matches(document, query)), None)

    async def insert_one(self, document: dict) -> SimpleNamespace:
        stored = {"_id": ObjectId(), **document}
        self.documents.append(stored)
        return SimpleNamespace(inserted_id=stored["_id"])

    async def delete_one(self, query: dict) -> SimpleNamespace:
        document = await self.find_one(query)
        if document is None:
            return SimpleNamespace(deleted_count=0)
        self.documents.remove(document)
        return SimpleNamespace(deleted_count=1)

    async def update_one(self, query: dict, changes: dict, upsert: bool = False) -> SimpleNamespace:
        document = await self.find_one(query)
        if document is None and upsert:
            document = {"_id": ObjectId(), **query, **changes.get("$setOnInsert", {})}
            self.documents.append(document)
        if document is None:
            return SimpleNamespace(modified_count=0)
        document.update(changes.get("$set", {}))
        return SimpleNamespace(modified_count=1)


class FakeDatabase:
    def __init__(self) -> None:
        self.collections: dict[str, FakeCollection] = {}

    def __getitem__(self, name: str) -> FakeCollection:
        return self.collections.setdefault(name, FakeCollection())


class AuthenticationApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from fastapi.testclient import TestClient

        cls.database = FakeDatabase()

        async def database_override():
            yield cls.database

        app.dependency_overrides[get_database] = database_override
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls) -> None:
        app.dependency_overrides.clear()

    def register_student(self) -> str:
        response = self.client.post("/api/v1/auth/register", json={
            "email": "student@example.test", "display_name": "Test Student", "password": "VerySecurePass!1",
            "student_number": "TEST-001", "program_code": "TEST", "program_name": "Testing",
        })
        self.assertEqual(response.status_code, 201)
        return response.json()["access_token"]

    def setUp(self) -> None:
        self.database.collections.clear()

    def test_successful_login(self) -> None:
        self.register_student()
        response = self.client.post("/api/v1/auth/login", json={"email": "student@example.test", "password": "VerySecurePass!1"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())

    def test_registration_ignores_frontend_role(self) -> None:
        response = self.client.post("/api/v1/auth/register", json={
            "email": "role@example.test", "display_name": "Role Test", "password": "VerySecurePass!1",
            "student_number": "TEST-ROLE", "program_code": "TEST", "program_name": "Testing", "role": "admin",
        })
        token = response.json()["access_token"]
        current = self.client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(current.json()["role"], "student")

    def test_invalid_password(self) -> None:
        self.register_student()
        response = self.client.post("/api/v1/auth/login", json={"email": "student@example.test", "password": "wrong"})
        self.assertEqual(response.status_code, 401)

    def test_missing_and_invalid_tokens(self) -> None:
        self.assertEqual(self.client.get("/api/v1/auth/me").status_code, 401)
        self.assertEqual(self.client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid"}).status_code, 401)

    def test_role_restrictions(self) -> None:
        teacher_id, admin_id = ObjectId(), ObjectId()
        self.database["users"].documents.extend([
            {"_id": teacher_id, "email": "teacher@example.test", "display_name": "Teacher", "role": "teacher", "active": True, "password_hash": hash_password("VerySecurePass!2")},
            {"_id": admin_id, "email": "admin@example.test", "display_name": "Admin", "role": "admin", "active": True, "password_hash": hash_password("VerySecurePass!3")},
        ])
        teacher_token = self.client.post("/api/v1/auth/login", json={"email": "teacher@example.test", "password": "VerySecurePass!2"}).json()["access_token"]
        admin_token = self.client.post("/api/v1/auth/login", json={"email": "admin@example.test", "password": "VerySecurePass!3"}).json()["access_token"]
        self.assertEqual(self.client.get("/api/v1/admin/access-check", headers={"Authorization": f"Bearer {teacher_token}"}).status_code, 403)
        self.assertEqual(self.client.get("/api/v1/admin/access-check", headers={"Authorization": f"Bearer {admin_token}"}).status_code, 200)
