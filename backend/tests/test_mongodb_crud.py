"""Optional integration test: requires a disposable MongoDB instance."""

import os
import sys
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path

from bson import ObjectId
from pymongo import AsyncMongoClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.models.collections import NOTIFICATIONS
from app.repositories.base import MongoRepository


@unittest.skipUnless(os.getenv("RUN_MONGO_INTEGRATION") == "1", "Set RUN_MONGO_INTEGRATION=1 with local MongoDB running")
class MongoRepositoryCrudTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.client = AsyncMongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"), serverSelectionTimeoutMS=5000)
        self.repository = MongoRepository(self.client[os.getenv("MONGODB_DATABASE", "prok")], NOTIFICATIONS)

    async def asyncTearDown(self) -> None:
        await self.client.close()

    async def test_notification_crud(self) -> None:
        identifier = await self.repository.create({
            "user_id": ObjectId(), "type": "system", "title": "Integration test", "body": "Temporary test record.",
            "read_at": None, "created_at": datetime.now(UTC), "expires_at": datetime.now(UTC) + timedelta(minutes=5),
        })
        try:
            self.assertIsNotNone(await self.repository.find_by_id(identifier))
            self.assertTrue(await self.repository.update_by_id(identifier, {"read_at": datetime.now(UTC)}))
        finally:
            self.assertTrue(await self.repository.delete_by_id(identifier))
        self.assertIsNone(await self.repository.find_by_id(identifier))
