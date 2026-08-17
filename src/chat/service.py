from src.chat.graph.state import ChatGraph, ChatState


class ChatService:
    def __init__(self, graph: ChatGraph) -> None:
        self._graph = graph

    async def ask(self, message: str) -> str:
        result = await self._graph.ainvoke(
            ChatState(
                message=message,
                answer="",
            )
        )

        return result["answer"]
