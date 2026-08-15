"""A LangGraph approval flow that keeps the payment side effect after interrupt()."""

from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class PaymentState(TypedDict):
    payment_id: str
    amount_cents: int
    approved: bool
    receipt_id: str


class PaymentGateway:
    """A tiny idempotent stand-in for a real payment API."""

    def __init__(self) -> None:
        self.receipts_by_key: dict[str, str] = {}

    def charge(self, amount_cents: int, idempotency_key: str) -> str:
        if idempotency_key not in self.receipts_by_key:
            self.receipts_by_key[idempotency_key] = f"receipt-{len(self.receipts_by_key) + 1}"
        return self.receipts_by_key[idempotency_key]


gateway = PaymentGateway()


def request_approval(state: PaymentState) -> dict:
    decision = interrupt(
        {
            "question": "Approve this payment?",
            "payment_id": state["payment_id"],
            "amount_cents": state["amount_cents"],
        }
    )
    return {"approved": bool(decision)}


def charge_after_approval(state: PaymentState) -> dict:
    if not state["approved"]:
        return {"receipt_id": "not-charged"}

    receipt_id = gateway.charge(
        amount_cents=state["amount_cents"],
        idempotency_key=state["payment_id"],
    )
    return {"receipt_id": receipt_id}


builder = StateGraph(PaymentState)
builder.add_node("request_approval", request_approval)
builder.add_node("charge_after_approval", charge_after_approval)
builder.add_edge(START, "request_approval")
builder.add_edge("request_approval", "charge_after_approval")
builder.add_edge("charge_after_approval", END)
graph = builder.compile(checkpointer=InMemorySaver())

config = {"configurable": {"thread_id": "payment-pay-1042"}}
paused = graph.invoke(
    {
        "payment_id": "pay-1042",
        "amount_cents": 4500,
        "approved": False,
        "receipt_id": "",
    },
    config,
)
finished = graph.invoke(Command(resume=True), config)

assert paused["__interrupt__"]
assert finished["receipt_id"] == "receipt-1"
assert gateway.charge(4500, "pay-1042") == "receipt-1"
