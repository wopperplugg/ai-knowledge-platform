from unittest.mock import AsyncMock

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from src.chat.graph.nodes import create_generate_node
from src.chat.graph.state import ChatState
from src.chat.llm import LLMClient


@pytest.mark.asyncio
async def test_generate_node_returns_llm_answer() -> None:
    llm = AsyncMock(spec=LLMClient)
    human_message = HumanMessage(content="What is RAG?")
    ai_message = AIMessage(content="RAG combines retrieval and generation.")
    llm.generate.return_value = ai_message

    node = create_generate_node(llm)

    result = await node(
        ChatState(
            messages=[human_message],
        )
    )

    assert result == {
        "messages": [ai_message],
    }

    llm.generate.assert_awaited_once_with([human_message])
