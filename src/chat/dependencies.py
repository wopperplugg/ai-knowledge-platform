from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from langchain_ollama import ChatOllama

from src.chat.graph.builder import build_chat_graph
from src.chat.graph.state import ChatGraph
from src.chat.llm import LLMClient, OllamaLLMClient
from src.chat.service import ChatService
from src.chat.workflow import LangGraphChatWorkflow
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


@lru_cache
def get_chat_graph(
    llm: Annotated[LLMClient, Depends(get_llm_client)],
) -> ChatGraph:
    return build_chat_graph(llm)


def get_chat_workflow(
    graph: Annotated[ChatGraph, Depends(get_chat_graph)],
) -> LangGraphChatWorkflow:
    return LangGraphChatWorkflow(graph=graph)


def get_chat_service(
    workflow: Annotated[LangGraphChatWorkflow, Depends(get_chat_workflow)],
) -> ChatService:
    return ChatService(workflow=workflow)
