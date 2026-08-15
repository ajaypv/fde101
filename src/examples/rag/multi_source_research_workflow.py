"""A deterministic multi-source research workflow.

All records below are synthetic fixtures. The example shows orchestration and
evidence checks; it does not compare real model quality or prices.
"""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class ResearchTask:
    question: str
    source: str


@dataclass(frozen=True)
class Evidence:
    source: str
    locator: str
    observed_at: str
    statement: str


ALLOWED_SOURCES = frozenset({"internal_docs", "benchmark_registry", "cost_sql"})
MAX_AGE_DAYS = {
    "internal_docs": 90,
    "benchmark_registry": 7,
    "cost_sql": 45,
}

FIXTURES = {
    "internal_docs": Evidence(
        source="internal_docs",
        locator="policy://ai/model-requirements-v3#security",
        observed_at="2026-08-15",
        statement="The selected path must support regional processing and citations.",
    ),
    "benchmark_registry": Evidence(
        source="benchmark_registry",
        locator="benchmark://rag-golden-set/run-184",
        observed_at="2026-08-15",
        statement="Model B passed 94 of 100 synthetic evaluation cases.",
    ),
    "cost_sql": Evidence(
        source="cost_sql",
        locator="sql://finance/model-costs/2026-07",
        observed_at="2026-08-01",
        statement="Model B cost 18 synthetic units per accepted answer.",
    ),
}


def make_plan() -> list[ResearchTask]:
    """These known requirements do not need an LLM planner."""
    return [
        ResearchTask("What constraints must the model satisfy?", "internal_docs"),
        ResearchTask("How does each candidate perform on our RAG eval set?", "benchmark_registry"),
        ResearchTask("What is the cost per accepted grounded answer?", "cost_sql"),
    ]


def retrieve(task: ResearchTask) -> Evidence:
    if task.source not in ALLOWED_SOURCES:
        raise PermissionError(f"source is not approved: {task.source}")
    return FIXTURES[task.source]


def validate_evidence(rows: list[Evidence], *, as_of: date) -> None:
    found = {row.source for row in rows}
    missing = ALLOWED_SOURCES - found
    if missing:
        raise RuntimeError(f"human review: missing evidence from {sorted(missing)}")
    if any(not row.locator or not row.observed_at for row in rows):
        raise RuntimeError("human review: evidence lacks provenance or date")
    for row in rows:
        try:
            observed_at = date.fromisoformat(row.observed_at)
        except ValueError as exc:
            raise RuntimeError("human review: evidence has an invalid date") from exc
        age_days = (as_of - observed_at).days
        if age_days < 0 or age_days > MAX_AGE_DAYS[row.source]:
            raise RuntimeError(f"human review: stale evidence from {row.source}")


def research() -> list[Evidence]:
    plan = make_plan()
    with ThreadPoolExecutor(max_workers=len(plan)) as pool:
        rows = list(pool.map(retrieve, plan))
    validate_evidence(rows, as_of=date(2026, 8, 15))
    return rows


if __name__ == "__main__":
    for evidence in research():
        print(f"[{evidence.source}] {evidence.statement}")
        print(f"  source: {evidence.locator} ({evidence.observed_at})")
