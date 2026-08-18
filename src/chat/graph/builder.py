from typing import Any, cast

from langgraph.graph import END, START, StateGraph

from src.chat.graph.nodes import create_generate_node
from src.chat.graph.state import ChatGraph, ChatState
from src.chat.llm import LLMClient


def build_chat_graph(llm: LLMClient) -> ChatGraph:
    graph = StateGraph(ChatState)
    graph.add_node("generate", cast(Any, create_generate_node(llm)))
    graph.add_edge(START, "generate")
    graph.add_edge("generate", END)

    return graph.compile()
