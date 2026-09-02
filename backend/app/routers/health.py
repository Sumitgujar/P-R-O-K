from fastapi import APIRouter, Depends
from pymongo.asynchronous.database import AsyncDatabase

from app.db.mongodb import get_database
from app.schemas.health import HealthResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse, summary="Check API and MongoDB connectivity")
async def health_check(database: AsyncDatabase = Depends(get_database)) -> HealthResponse:
    await database.command("ping")
    return HealthResponse(status="ok", service="prok-api", database="connected")
