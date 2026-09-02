"""Create structural MongoDB indexes; this script does not seed data."""

import asyncio
import os
import sys
from pathlib import Path

from pymongo import AsyncMongoClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from indexes import INDEXES  # noqa: E402


async def main() -> None:
    uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    database_name = os.getenv("MONGODB_DATABASE", "prok")
    client = AsyncMongoClient(uri, serverSelectionTimeoutMS=5000)
    try:
        database = client[database_name]
        for collection, definitions in INDEXES.items():
            for keys, options in definitions:
                await database[collection].create_index(keys, **options)
        print(f"Created PROK indexes in '{database_name}'.")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
