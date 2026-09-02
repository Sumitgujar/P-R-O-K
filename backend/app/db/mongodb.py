from collections.abc import AsyncIterator

from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import get_settings


class MongoDatabase:
    """Owns the async MongoDB client for the FastAPI process."""

    def __init__(self) -> None:
        self.client: AsyncMongoClient | None = None

    async def connect(self) -> None:
        settings = get_settings()
        self.client = AsyncMongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=5000)
        # Fail early on a malformed/unavailable local database configuration.
        await self.client.admin.command("ping")

    async def close(self) -> None:
        if self.client is not None:
            await self.client.close()
            self.client = None

    def database(self) -> AsyncDatabase:
        if self.client is None:
            raise RuntimeError("MongoDB client is not connected")
        return self.client[get_settings().mongodb_database]


mongo = MongoDatabase()


async def get_database() -> AsyncIterator[AsyncDatabase]:
    yield mongo.database()
