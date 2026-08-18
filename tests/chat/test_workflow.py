import pytest
from langchain_core.messages import AIMessage, HumanMessage

from src.chat.graph.state import ChatState
from src.chat.workflow import ChatWorkflowError, LangGraphChatWorkflow


class SuccessfulGraph:
    def __init__(self) -> None:
        self.input_state: ChatState | None = None

    async def ainvoke(self, input: ChatState) -> ChatState:
        self.input_state = input
        messages = input["messages"]

        return ChatState(messages=[*messages, AIMessage(content="workflow answer")])


class EmptyGraph:
    async def ainvoke(self, input: ChatState) -> ChatState:
        return ChatState(messages=[])


class NonAIResponseGraph:
    async def ainvoke(self, input: ChatState) -> ChatState:
        return ChatState(messages=[HumanMessage(content="not ai")])


class EmptyAIResponseGraph:
    async def ainvoke(self, input: ChatState) -> ChatState:
        return ChatState(messages=[AIMessage(content="")])


@pytest.mark.asyncio
async def test_langgraph_chat_workflow_converts_string_to_human_message() -> None:
    graph = SuccessfulGraph()
    workflow = LangGraphChatWorkflow(graph=graph)

    result = await workflow.run("question")

    assert result == "workflow answer"
    assert graph.input_state is not None
    messages = graph.input_state["messages"]
    assert len(messages) == 1
    assert isinstance(messages[0], HumanMessage)
    assert messages[0].content == "question"


@pytest.mark.parametrize(
    "graph",
    [
        EmptyGraph(),
        NonAIResponseGraph(),
        EmptyAIResponseGraph(),
    ],
)
async def test_langgraph_chat_workflow_rejects_invalid_final_state(
    graph: EmptyGraph | NonAIResponseGraph | EmptyAIResponseGraph,
) -> None:
    workflow = LangGraphChatWorkflow(graph=graph)

    with pytest.raises(ChatWorkflowError):
        await workflow.run("question")
