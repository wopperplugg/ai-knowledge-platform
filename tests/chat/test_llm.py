from unittest.mock import AsyncMock

import pytest

from src.chat.service import ChatService
from src.chat.workflow import ChatWorkflow


@pytest.mark.asyncio
async def test_ask_returns_llm_response() -> None:
    workflow = AsyncMock(spec=ChatWorkflow)
    workflow.run.return_value = "RAG combines retrieval and generation"

    service = ChatService(workflow=workflow)

    result = await service.ask("what is rag")

    assert result == "RAG combines retrieval and generation"
    workflow.run.assert_awaited_once_with("what is rag")
