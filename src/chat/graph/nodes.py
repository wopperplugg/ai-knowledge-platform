from collections.abc import Awaitable, Callable

from src.chat.graph.state import ChatState
from src.chat.llm import LLMClient

GenerateNode = Callable[[ChatState], Awaitable[dict[str, str]]]


def create_generate_node(llm: LLMClient) -> GenerateNode:
    async def generate(state: ChatState) -> dict[str, str]:
        answer = await llm.generate(state["message"])

        return {"answer": answer}

    return generate
