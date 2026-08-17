from unittest.mock import AsyncMock

import pytest

from src.chat.graph.builder import build_chat_graph
from src.chat.llm import LLMClient


@pytest.mark.asyncio
async def test_chat_graph_generates_answer() -> None:
    llm = AsyncMock(spec=LLMClient)
    llm.generate.return_value = "Generated answer"

    graph = build_chat_graph(llm)

    result = await graph.ainvoke(
        {
            "message": "Hello",
            "answer": "",
        }
    )

    assert result["message"] == "Hello"
    assert result["answer"] == "Generated answer"
