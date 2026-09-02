from collections.abc import Mapping
from typing import Any

from bson import ObjectId
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase


class MongoRepository:
    """Small repository primitive; business services own collection semantics."""

    def __init__(self, database: AsyncDatabase, collection_name: str) -> None:
        self.collection: AsyncCollection = database[collection_name]

    async def create(self, document: Mapping[str, Any]) -> ObjectId:
        result = await self.collection.insert_one(dict(document))
        return result.inserted_id

    async def find_by_id(self, identifier: ObjectId) -> dict[str, Any] | None:
        return await self.collection.find_one({"_id": identifier})

    async def update_by_id(self, identifier: ObjectId, changes: Mapping[str, Any]) -> bool:
        result = await self.collection.update_one({"_id": identifier}, {"$set": dict(changes)})
        return result.modified_count == 1

    async def delete_by_id(self, identifier: ObjectId) -> bool:
        result = await self.collection.delete_one({"_id": identifier})
        return result.deleted_count == 1
