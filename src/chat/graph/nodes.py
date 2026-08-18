from collections.abc import Awaitable, Callable

from src.chat.graph.state import ChatState
from src.chat.llm import LLMClient

GenerateNode = Callable[[ChatState], Awaitable[ChatState]]


def create_generate_node(llm: LLMClient) -> GenerateNode:
    async def generate(state: ChatState) -> ChatState:
        response = await llm.generate(state["messages"])

        return ChatState(messages=[response])

    return generate
