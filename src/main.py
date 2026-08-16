from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.config import get_settings
from src.core.database import close_database_engine
from src.health.router import ReadinessChecker, create_health_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    await close_database_engine()


def create_app(readiness_checker: ReadinessChecker | None = None) -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )

    if readiness_checker is None:
        app.include_router(create_health_router())
    else:

        async def get_readiness_checker() -> ReadinessChecker:
            return readiness_checker

        app.include_router(create_health_router(get_readiness_checker))

    return app


app = create_app()
