from collections.abc import Awaitable
from typing import Protocol

from langgraph.graph import MessagesState


class ChatState(MessagesState):
    pass


class ChatGraph(Protocol):
    def ainvoke(self, input: ChatState) -> Awaitable[object]: ...
