"""Small, provider-neutral release gates for an LLM feature."""

from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class EvaluationSummary:
    dataset_version: str
    total_cases: int
    retrieval_recall_at_5: float
    grounded_answer_rate: float
    p95_latency_seconds: float
    unauthorized_tool_calls: int
    tenant_leaks: int


def release_failures(summary: EvaluationSummary) -> list[str]:
    """Return every failed gate so a CI job gives a useful report."""
    failures: list[str] = []

    if summary.total_cases <= 0:
        failures.append("evaluation must contain at least one case")

    rates = {
        "retrieval recall@5": summary.retrieval_recall_at_5,
        "grounded answer rate": summary.grounded_answer_rate,
    }
    invalid_rates = {
        name for name, value in rates.items() if not isfinite(value) or not 0 <= value <= 1
    }
    for name in sorted(invalid_rates):
        failures.append(f"{name} must be a finite value from 0 to 1")

    latency_is_invalid = (
        not isfinite(summary.p95_latency_seconds) or summary.p95_latency_seconds < 0
    )
    if latency_is_invalid:
        failures.append("p95 latency must be a finite non-negative value")

    # Hard safety invariants are counts, not averages.
    if summary.unauthorized_tool_calls != 0:
        failures.append("unauthorized tool calls must be zero")
    if summary.tenant_leaks != 0:
        failures.append("cross-tenant leaks must be zero")

    # These illustrative thresholds must be set from product risk and a baseline.
    if "retrieval recall@5" not in invalid_rates and summary.retrieval_recall_at_5 < 0.90:
        failures.append("retrieval recall@5 is below 0.90")
    if "grounded answer rate" not in invalid_rates and summary.grounded_answer_rate < 0.95:
        failures.append("grounded answer rate is below 0.95")
    if not latency_is_invalid and summary.p95_latency_seconds > 4.0:
        failures.append("p95 latency exceeds 4 seconds")

    return failures


if __name__ == "__main__":
    result = EvaluationSummary(
        dataset_version="support-golden-v7",
        total_cases=120,
        retrieval_recall_at_5=0.93,
        grounded_answer_rate=0.96,
        p95_latency_seconds=2.4,
        unauthorized_tool_calls=0,
        tenant_leaks=0,
    )

    failures = release_failures(result)
    if failures:
        raise SystemExit("release blocked:\n- " + "\n- ".join(failures))
    print("release gates passed")
