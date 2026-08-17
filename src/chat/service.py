from src.chat.llm import LLMClient


class ChatService:
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    async def ask(self, message: str) -> str:
        return await self._llm.generate(message)
