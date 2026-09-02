from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.mongodb import mongo
from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.access import router as access_router

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    await mongo.connect()
    yield
    await mongo.close()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(health_router, prefix=settings.api_v1_prefix)
app.include_router(auth_router, prefix=settings.api_v1_prefix)
app.include_router(access_router, prefix=settings.api_v1_prefix)
