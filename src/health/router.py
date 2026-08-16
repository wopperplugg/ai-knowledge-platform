from collections.abc import Awaitable, Callable
from typing import Annotated, Protocol

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_database_session
from src.health.service import HealthService


class ReadinessChecker(Protocol):
    async def is_database_ready(self) -> bool: ...


async def get_health_service(
    session: Annotated[AsyncSession, Depends(get_database_session)],
) -> HealthService:
    return HealthService(session=session)


def create_health_router(
    health_service_dependency: Callable[..., Awaitable[ReadinessChecker]] = get_health_service,
) -> APIRouter:
    router = APIRouter(prefix="/health", tags=["health"])

    @router.get("/live", status_code=status.HTTP_200_OK)
    async def liveness() -> dict[str, str]:
        return {"status": "ok"}

    @router.get("/ready", status_code=status.HTTP_200_OK, response_model=None)
    async def readiness(
        health_service: Annotated[ReadinessChecker, Depends(health_service_dependency)],
    ) -> dict[str, str] | JSONResponse:
        if not await health_service.is_database_ready():
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"status": "unavailable", "database": "unavailable"},
            )

        return {"status": "ok", "database": "ok"}

    return router
