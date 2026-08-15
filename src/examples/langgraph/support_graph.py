"""A minimal LangGraph workflow with explicit, inspectable state."""

from typing import Literal, TypedDict

from langgraph.graph import END, START, StateGraph


class SupportState(TypedDict):
    question: str
    category: Literal["invoice", "general"]
    response: str


def classify(state: SupportState) -> dict:
    category = "invoice" if "invoice" in state["question"].lower() else "general"
    return {"category": category}


def draft_response(state: SupportState) -> dict:
    if state["category"] == "invoice":
        response = "I will look up the invoice and cite the matching record."
    else:
        response = "I will search the support knowledge base before answering."
    return {"response": response}


builder = StateGraph(SupportState)
builder.add_node("classify", classify)
builder.add_node("draft_response", draft_response)
builder.add_edge(START, "classify")
builder.add_edge("classify", "draft_response")
builder.add_edge("draft_response", END)

graph = builder.compile()

result = graph.invoke(
    {"question": "Why is invoice 1042 duplicated?", "category": "general", "response": ""}
)
print(result["response"])
