from unittest.mock import AsyncMock

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from src.chat.graph.builder import build_chat_graph
from src.chat.graph.state import ChatState
from src.chat.llm import LLMClient


@pytest.mark.asyncio
async def test_chat_graph_generates_answer() -> None:
    llm = AsyncMock(spec=LLMClient)
    ai_message = AIMessage(content="Generated answer")
    llm.generate.return_value = ai_message

    graph = build_chat_graph(llm)

    result = await graph.ainvoke(
        ChatState(
            messages=[HumanMessage(content="Hello")],
        )
    )

    assert isinstance(result, dict)
    assert len(result["messages"]) == 2
    assert isinstance(result["messages"][0], HumanMessage)
    assert result["messages"][0].content == "Hello"
    assert result["messages"][1] == ai_message
    llm.generate.assert_awaited_once()
