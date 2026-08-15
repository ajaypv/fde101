"""A provider-neutral retrieval pipeline with visible production stages."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Passage:
    id: str
    text: str
    source: str


class SearchIndex(Protocol):
    def keyword_search(
        self, query: str, *, k: int, filters: dict[str, str]
    ) -> list[Passage]: ...

    def vector_search(
        self, query: str, *, k: int, filters: dict[str, str]
    ) -> list[Passage]: ...


class QueryRewriter(Protocol):
    def rewrite(self, question: str) -> str: ...


class Reranker(Protocol):
    def rank(self, question: str, passages: list[Passage]) -> list[Passage]: ...


class LanguageModel(Protocol):
    def answer(self, question: str, context: str) -> str: ...


def reciprocal_rank_fusion(
    result_lists: list[list[Passage]], *, rank_constant: int = 60
) -> list[Passage]:
    """Merge rankings without assuming their raw scores are comparable."""
    scores: dict[str, float] = {}
    passages_by_id: dict[str, Passage] = {}

    for results in result_lists:
        for rank, passage in enumerate(results, start=1):
            scores[passage.id] = scores.get(passage.id, 0.0) + 1 / (
                rank_constant + rank
            )
            passages_by_id[passage.id] = passage

    return sorted(passages_by_id.values(), key=lambda item: scores[item.id], reverse=True)


def answer_with_production_retrieval(
    question: str,
    *,
    tenant_id: str,
    principal_id: str,
    index: SearchIndex,
    rewriter: QueryRewriter,
    reranker: Reranker,
    model: LanguageModel,
) -> tuple[str, list[Passage]]:
    # The search adapter must enforce both isolation and caller-level access.
    filters = {"tenant_id": tenant_id, "principal_id": principal_id}
    rewritten_query = rewriter.rewrite(question)

    # Keep the original query for exact IDs; use the rewrite for semantic recall.
    keyword_results = index.keyword_search(question, k=20, filters=filters)
    vector_results = index.vector_search(rewritten_query, k=20, filters=filters)

    fused = reciprocal_rank_fusion([keyword_results, vector_results])
    final_passages = reranker.rank(question, fused[:30])[:5]

    if not final_passages:
        return "I could not find enough evidence to answer.", []

    passages = "\n\n".join(
        f"[{number}] {passage.text}\nSource: {passage.source}"
        for number, passage in enumerate(final_passages, start=1)
    )
    context = (
        "Answer only from the passages below. Cite passage numbers like [1]. "
        "If they are insufficient, say you do not have enough evidence.\n\n"
        + passages
    )
    answer = model.answer(question, context)

    # Return the exact passages so another stage can check claims and citations.
    return answer, final_passages
