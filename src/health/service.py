import logging
from asyncio import timeout

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class HealthService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def is_database_ready(self) -> bool:
        try:
            async with timeout(2.0):
                await self._session.execute(text("SELECT 1"))
        except (SQLAlchemyError, TimeoutError):
            logger.exception("Database readiness check failed")
            return False

        return True
