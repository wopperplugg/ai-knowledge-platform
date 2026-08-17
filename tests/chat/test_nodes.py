from unittest.mock import AsyncMock

import pytest

from src.chat.graph.nodes import create_generate_node
from src.chat.llm import LLMClient


@pytest.mark.asyncio
async def test_generate_node_returns_llm_answer() -> None:
    llm = AsyncMock(spec=LLMClient)
    llm.generate.return_value = "RAG combines retrieval and generation."

    node = create_generate_node(llm)

    result = await node(
        {
            "message": "What is RAG?",
            "answer": "",
        }
    )

    assert result == {
        "answer": "RAG combines retrieval and generation.",
    }

    llm.generate.assert_awaited_once_with("What is RAG?")
