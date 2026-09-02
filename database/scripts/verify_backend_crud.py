"""Exercise MongoDB create/read/update/delete through the backend repository layer."""

import asyncio
import os
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

from bson import ObjectId
from pymongo import AsyncMongoClient

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend"))
from app.models.collections import NOTIFICATIONS  # noqa: E402
from app.repositories.base import MongoRepository  # noqa: E402


async def main() -> None:
    client = AsyncMongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"), serverSelectionTimeoutMS=5000)
    try:
        database = client[os.getenv("MONGODB_DATABASE", "prok")]
        repository = MongoRepository(database, NOTIFICATIONS)
        notification_id = await repository.create({
            "user_id": ObjectId(), "type": "system", "title": "CRUD smoke test", "body": "Temporary test record.",
            "read_at": None, "created_at": datetime.now(UTC), "expires_at": datetime.now(UTC) + timedelta(minutes=10),
            "is_crud_smoke_test": True,
        })
        try:
            created = await repository.find_by_id(notification_id)
            assert created is not None and created["title"] == "CRUD smoke test"
            assert await repository.update_by_id(notification_id, {"read_at": datetime.now(UTC)})
            updated = await repository.find_by_id(notification_id)
            assert updated is not None and updated["read_at"] is not None
        finally:
            assert await repository.delete_by_id(notification_id)
        assert await repository.find_by_id(notification_id) is None
        print("Backend MongoDB CRUD smoke test passed.")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
