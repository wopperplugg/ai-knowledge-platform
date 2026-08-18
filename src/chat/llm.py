import logging
from collections.abc import Sequence
from typing import Protocol

import httpx
from langchain_core.messages import AIMessage, BaseMessage, SystemMessage
from langchain_ollama import ChatOllama

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Ты ассистент-помощник для корпоративной базы знаний. "
    "Отвечай чисто и по делу. "
    "Если ты не знаешь ответ, скажи что ты не знаешь. "
)


class LLMClient(Protocol):
    async def generate(self, messages: Sequence[BaseMessage]) -> AIMessage: ...


class OllamaLLMClient:
    def __init__(self, model: ChatOllama) -> None:
        self._model = model

    async def generate(self, messages: Sequence[BaseMessage]) -> AIMessage:
        try:
            response = await self._model.ainvoke(
                [
                    SystemMessage(content=SYSTEM_PROMPT),
                    *messages,
                ]
            )
        except httpx.HTTPError as exc:
            logger.exception("Ollama request failed")
            raise RuntimeError("LLM service is unavailable") from exc

        if not response.text:
            raise RuntimeError("LLM вернула пустой ответ")

        return response
