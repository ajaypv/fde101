"""A small agent loop whose authority stays in application code."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, str]


@dataclass(frozen=True)
class FinalAnswer:
    text: str


Decision = ToolCall | FinalAnswer


class AgentModel(Protocol):
    def decide(
        self, messages: list[dict[str, str]], tools: tuple[str, ...]
    ) -> Decision: ...


def search_knowledge_base(query: str) -> str:
    return f"Approved knowledge-base results for: {query}"


def lookup_order(order_id: str) -> str:
    return f"Authorized status for order: {order_id}"


def execute_tool(call: ToolCall) -> str:
    """Validate model-produced arguments before executing a scoped tool."""
    if call.name == "search_knowledge_base":
        query = call.arguments.get("query", "").strip()
        if not query:
            raise ValueError("query is required")
        return search_knowledge_base(query)

    if call.name == "lookup_order":
        order_id = call.arguments.get("order_id", "").strip()
        if not order_id.startswith("ORD-"):
            raise ValueError("order_id must start with ORD-")
        # A real application would also verify that the user owns this order.
        return lookup_order(order_id)

    raise ValueError(f"Tool is not allowed: {call.name}")


def run_agent(question: str, *, model: AgentModel, max_steps: int = 5) -> str:
    messages = [{"role": "user", "content": question}]
    allowed_tools = ("search_knowledge_base", "lookup_order")

    for _ in range(max_steps):
        decision = model.decide(messages, allowed_tools)

        if isinstance(decision, FinalAnswer):
            return decision.text

        observation = execute_tool(decision)
        messages.append({"role": "assistant", "content": repr(decision)})
        messages.append({"role": "tool", "content": observation})

    return "Stopped after the step limit; a human should review this task."
