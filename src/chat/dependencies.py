from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from langchain_ollama import ChatOllama

from src.chat.llm import OllamaLLMClient
from src.chat.service import ChatService
from src.core.config import get_settings


@lru_cache
def get_chat_model() -> ChatOllama:
    settings = get_settings()

    return ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_base_url,
        temperature=0,
    )


def get_llm_client(
    model: Annotated[ChatOllama, Depends(get_chat_model)],
) -> OllamaLLMClient:
    return OllamaLLMClient(model=model)


def get_chat_service(
    llm: Annotated[OllamaLLMClient, Depends(get_llm_client)],
) -> ChatService:
    return ChatService(llm=llm)
