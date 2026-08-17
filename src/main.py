from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from src.chat.router import create_chat_router
from src.core.config import get_settings
from src.core.database import close_database_engine
from src.health.router import ReadinessChecker, create_health_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    await close_database_engine()


def create_app(
    readiness_checker: ReadinessChecker | None = None,
    chat_service_dependency: Callable[..., Any] | None = None,
) -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )

    if readiness_checker is None:
        app.include_router(create_health_router())
        if chat_service_dependency is None:
            app.include_router(create_chat_router())
        else:
            app.include_router(create_chat_router(chat_service_dependency))
    else:

        async def get_readiness_checker() -> ReadinessChecker:
            return readiness_checker

        app.include_router(create_health_router(get_readiness_checker))

    return app


app = create_app()
