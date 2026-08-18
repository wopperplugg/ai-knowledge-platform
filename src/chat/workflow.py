from collections.abc import Mapping
from typing import Protocol

from langchain_core.messages import AIMessage, HumanMessage

from src.chat.graph.state import ChatGraph, ChatState


class ChatWorkflowError(RuntimeError):
    pass


class ChatWorkflow(Protocol):
    async def run(self, message: str) -> str: ...


class LangGraphChatWorkflow:
    def __init__(self, graph: ChatGraph) -> None:
        self._graph = graph

    async def run(self, message: str) -> str:
        state = await self._graph.ainvoke(
            ChatState(
                messages=[HumanMessage(content=message)],
            )
        )

        if not isinstance(state, Mapping):
            raise ChatWorkflowError("Chat workflow returned invalid state")

        messages = state.get("messages")

        if not isinstance(messages, list) or not messages:
            raise ChatWorkflowError("Chat workflow returned no messages")

        response = messages[-1]
        if not isinstance(response, AIMessage):
            raise ChatWorkflowError("Chat workflow did not return an AI response")

        answer = str(response.text)
        if not answer:
            raise ChatWorkflowError("Chat workflow returned an empty AI response")

        return answer
