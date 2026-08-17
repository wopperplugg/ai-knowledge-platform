from typing import Annotated

from pydantic import BaseModel, StringConstraints

ChatMessage = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=4000,
    ),
]


class ChatRequest(BaseModel):
    message: ChatMessage


class ChatResponse(BaseModel):
    answer: str
