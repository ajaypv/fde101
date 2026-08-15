"""Build a small, inspectable context packet for a coding task."""

from dataclasses import dataclass
from datetime import date
from typing import Literal


Sensitivity = Literal["public", "internal", "secret"]


@dataclass(frozen=True)
class ContextItem:
    path: str
    tags: frozenset[str]
    token_estimate: int
    last_verified: date
    sensitivity: Sensitivity = "internal"


def item(
    path: str,
    tags: str,
    tokens: int,
    verified: str = "2026-08-15",
    sensitivity: Sensitivity = "internal",
) -> ContextItem:
    """Keep the synthetic fixtures short enough to scan in the lesson."""
    return ContextItem(
        path=path,
        tags=frozenset(tags.split()),
        token_estimate=tokens,
        last_verified=date.fromisoformat(verified),
        sensitivity=sensitivity,
    )


FILES = (
    item("app/api/auth.py", "auth fastapi route", 65, "2026-08-14"),
    item("app/security/jwt.py", "auth jwt api", 55),
    item("app/models/user.py", "auth user-model", 45, "2026-08-10"),
    item("tests/test_auth.py", "auth tests", 60),
    item("pyproject.toml", "conventions", 25, "2026-08-01"),
    item(".env", "auth jwt", 12, sensitivity="secret"),
    item("docs/legacy-oauth.md", "auth oauth", 110, "2025-10-01"),
    item("app/billing/invoices.py", "billing", 90),
)


def select_context(
    candidates: tuple[ContextItem, ...],
    needed_tags: frozenset[str],
    *,
    as_of: date,
    max_age_days: int,
    token_budget: int,
) -> tuple[tuple[ContextItem, ...], tuple[tuple[str, str], ...]]:
    """Select relevant, allowed, fresh items without exceeding the budget."""
    ranked: list[tuple[int, ContextItem]] = []
    rejected: list[tuple[str, str]] = []

    for candidate in candidates:
        if candidate.sensitivity == "secret":
            rejected.append((candidate.path, "blocked: secret"))
            continue

        age_days = (as_of - candidate.last_verified).days
        if age_days > max_age_days:
            rejected.append((candidate.path, f"blocked: stale ({age_days} days)"))
            continue

        overlap = len(candidate.tags & needed_tags)
        if overlap == 0:
            rejected.append((candidate.path, "skipped: irrelevant"))
            continue

        # Prefer more matching signals, then the smaller item. The path breaks
        # exact ties, so identical inputs always produce an identical packet.
        score = overlap * 1000 - candidate.token_estimate
        ranked.append((score, candidate))

    selected: list[ContextItem] = []
    used_tokens = 0
    for _, candidate in sorted(ranked, key=lambda pair: (-pair[0], pair[1].path)):
        if used_tokens + candidate.token_estimate > token_budget:
            rejected.append((candidate.path, "skipped: budget"))
            continue
        selected.append(candidate)
        used_tokens += candidate.token_estimate

    return tuple(selected), tuple(rejected)


if __name__ == "__main__":
    prompt = {
        "task": "Add POST /auth/refresh to the existing FastAPI service.",
        "instructions": "Reuse existing JWT helpers; preserve behavior; add tests.",
        "output_contract": "Return a patch, tests, and unresolved assumptions.",
    }
    selected, rejected = select_context(
        FILES,
        frozenset(
            {"auth", "fastapi", "route", "jwt", "api", "user-model", "tests", "conventions"}
        ),
        as_of=date(2026, 8, 15),
        max_age_days=120,
        token_budget=250,
    )

    print(f"TASK: {prompt['task']}")
    print("\nSELECTED CONTEXT")
    for context_item in selected:
        print(f"- {context_item.path} ({context_item.token_estimate} estimated tokens)")
    print("\nREJECTED CONTEXT")
    for path, reason in rejected:
        print(f"- {path}: {reason}")
