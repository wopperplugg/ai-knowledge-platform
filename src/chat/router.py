from collections.abc import Callable
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status

from src.chat.dependencies import get_chat_service
from src.chat.schemas import ChatRequest, ChatResponse
from src.chat.service import ChatService


def create_chat_router(
    chat_service_dependency: Callable[..., Any] = get_chat_service,
) -> APIRouter:
    router = APIRouter(
        prefix="/api/v1/chat",
        tags=["chat"],
    )

    @router.post(
        "",
        response_model=ChatResponse,
        status_code=status.HTTP_200_OK,
    )
    async def chat(
        payload: ChatRequest,
        service: Annotated[ChatService, Depends(chat_service_dependency)],
    ) -> ChatResponse:
        try:
            answer = await service.ask(payload.message)
        except RuntimeError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="LLM сервис вернул невалидный ответ",
            ) from exc
        return ChatResponse(answer=answer)

    return router
