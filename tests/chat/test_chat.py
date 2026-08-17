from collections.abc import Awaitable, Callable
from typing import cast

import pytest
from fastapi import HTTPException
from fastapi.routing import APIRoute
from pydantic import ValidationError

from src.chat.llm import LLMClient
from src.chat.router import create_chat_router
from src.chat.schemas import ChatRequest, ChatResponse
from src.chat.service import ChatService


class SuccessfulLLMClient:
    async def generate(self, message: str) -> str:
        return f"answer: {message}"


class FailingLLMClient:
    async def generate(self, message: str) -> str:
        raise RuntimeError("LLM service is unavailable")


def get_chat_endpoint() -> Callable[[ChatRequest, ChatService], Awaitable[ChatResponse]]:
    router = create_chat_router()
    route = next(route for route in router.routes if isinstance(route, APIRoute))
    return cast(Callable[[ChatRequest, ChatService], Awaitable[ChatResponse]], route.endpoint)


async def test_chat_returns_answer() -> None:
    endpoint = get_chat_endpoint()
    service = ChatService(llm=cast(LLMClient, SuccessfulLLMClient()))

    response = await endpoint(ChatRequest(message="hello"), service)

    assert response == ChatResponse(answer="answer: hello")


def test_chat_request_rejects_blank_message() -> None:
    with pytest.raises(ValidationError):
        ChatRequest(message="   ")


async def test_chat_raises_502_when_llm_fails() -> None:
    endpoint = get_chat_endpoint()
    service = ChatService(llm=cast(LLMClient, FailingLLMClient()))

    with pytest.raises(HTTPException) as exc_info:
        await endpoint(ChatRequest(message="hello"), service)

    assert exc_info.value.status_code == 502
    assert exc_info.value.detail == "LLM сервис вернул невалидный ответ"
