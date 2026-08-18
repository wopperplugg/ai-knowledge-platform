from src.chat.workflow import ChatWorkflow


class ChatService:
    def __init__(self, workflow: ChatWorkflow) -> None:
        self._workflow = workflow

    async def ask(self, message: str) -> str:
        return await self._workflow.run(message)
