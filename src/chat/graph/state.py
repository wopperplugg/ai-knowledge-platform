from collections.abc import Awaitable
from typing import Any, Protocol, TypedDict


class ChatState(TypedDict):
    message: str
    answer: str


class ChatGraph(Protocol):
    def ainvoke(self, input: ChatState, *args: Any, **kwargs: Any) -> Awaitable[ChatState]: ...
