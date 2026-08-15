"""A deliberately conservative semantic response-cache policy."""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Callable, Sequence


Vector = Sequence[float]


@dataclass(frozen=True)
class CacheScope:
    tenant_id: str
    authorization_scope: str
    route: str
    locale: str
    policy_version: str
    prompt_version: str
    model_version: str
    knowledge_version: str


@dataclass(frozen=True)
class CacheEntry:
    scope: CacheScope
    query_vector: Vector
    answer: str
    created_at: datetime


def safe_to_cache(*, route: str, has_personal_data: bool, has_side_effect: bool) -> bool:
    """Cache only stable, read-only FAQ responses in this example."""
    return route == "public_faq" and not has_personal_data and not has_side_effect


def add_cached_answer(
    entries: list[CacheEntry],
    *,
    scope: CacheScope,
    query_vector: Vector,
    answer: str,
    has_personal_data: bool,
    has_side_effect: bool,
    now: datetime | None = None,
) -> bool:
    """Insert only after the route-level cache policy accepts the response."""
    if not safe_to_cache(
        route=scope.route,
        has_personal_data=has_personal_data,
        has_side_effect=has_side_effect,
    ):
        return False

    entries.append(
        CacheEntry(
            scope=scope,
            query_vector=query_vector,
            answer=answer,
            created_at=now or datetime.now(UTC),
        )
    )
    return True


def find_cached_answer(
    entries: list[CacheEntry],
    *,
    scope: CacheScope,
    query_vector: Vector,
    similarity: Callable[[Vector, Vector], float],
    threshold: float,
    max_age: timedelta,
    now: datetime | None = None,
) -> str | None:
    """Return a scoped, fresh answer only when similarity clears the tested threshold."""
    current_time = now or datetime.now(UTC)
    candidates = [
        entry
        for entry in entries
        if entry.scope == scope and current_time - entry.created_at <= max_age
    ]
    if not candidates:
        return None

    best = max(candidates, key=lambda entry: similarity(query_vector, entry.query_vector))
    if similarity(query_vector, best.query_vector) < threshold:
        return None
    return best.answer


# Production code also needs encryption, deletion, audit records, concurrency
# control, and an evaluation of false hits and stale hits.
