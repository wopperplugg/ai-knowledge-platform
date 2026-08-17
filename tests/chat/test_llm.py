from unittest.mock import AsyncMock

import pytest

from src.chat.graph.builder import build_chat_graph
from src.chat.llm import LLMClient
from src.chat.service import ChatService


@pytest.mark.asyncio
async def test_ask_returns_llm_response() -> None:
    llm = AsyncMock(spec=LLMClient)
    llm.generate.return_value = "RAG combines retrieval and generation"

    service = ChatService(graph=build_chat_graph(llm))

    result = await service.ask("what is rag")

    assert result == "RAG combines retrieval and generation"
    llm.generate.assert_awaited_once_with("what is rag")
