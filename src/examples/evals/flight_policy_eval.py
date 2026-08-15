"""Separate retrieval failure from generation failure in a tiny RAG eval."""

from dataclasses import dataclass


QUESTION = "My flight is delayed by six hours. Am I eligible for a free hotel?"
GOLD_POLICY = (
    "Hotel accommodation is provided only when the delay requires an overnight "
    "stay and the airline caused the delay."
)
RELEVANT_POLICY_IDS = {"hotel-policy"}
K = 3


@dataclass(frozen=True)
class AnswerLabels:
    # None means the isolated generation check was intentionally not run.
    faithfulness: bool | None
    answer_relevance: bool | None
    correctness: bool | None


@dataclass(frozen=True)
class EvalRun:
    name: str
    retrieved_ids: list[str]
    answer: str
    labels: AnswerLabels


@dataclass(frozen=True)
class RetrievalScores:
    relevant_found: int
    precision_denominator: int
    recall_denominator: int
    hit_at_k: int
    precision_at_k: float
    recall_at_k: float


def retrieval_metrics(
    retrieved_ids: list[str], relevant_ids: set[str], k: int
) -> RetrievalScores:
    """Return both fractions and scores so the denominators stay visible."""
    if k <= 0 or len(retrieved_ids) < k:
        raise ValueError("k must be positive and no larger than the result list")
    if not relevant_ids:
        raise ValueError("use an abstention eval when no relevant item exists")

    top_k = retrieved_ids[:k]
    if len(set(top_k)) != k:
        raise ValueError("the top-k list must not contain duplicate IDs")

    relevant_found = sum(item in relevant_ids for item in top_k)
    return RetrievalScores(
        relevant_found=relevant_found,
        precision_denominator=k,
        recall_denominator=len(relevant_ids),
        hit_at_k=int(relevant_found > 0),
        precision_at_k=relevant_found / k,
        recall_at_k=relevant_found / len(relevant_ids),
    )


def diagnose(run: EvalRun) -> str:
    scores = retrieval_metrics(run.retrieved_ids, RELEVANT_POLICY_IDS, K)

    print(f"\n{run.name}")
    print(f"  Hit@{K}:       {scores.hit_at_k}")
    print(
        f"  Precision@{K}: {scores.relevant_found}/"
        f"{scores.precision_denominator} = {scores.precision_at_k:.3f}"
    )
    print(
        f"  Recall@{K}:    {scores.relevant_found}/"
        f"{scores.recall_denominator} = {scores.recall_at_k:.3f}"
    )
    print(f"  Answer: {run.answer}")
    print(f"  Answer labels: {run.labels}")

    if scores.recall_at_k < 1.0:
        return "retrieval failure: the gold policy never reached the model"
    if run.labels != AnswerLabels(True, True, True):
        return "generation failure: retrieval passed, but an answer label failed"
    return "case-level pass: needed evidence and all answer labels passed"


runs = [
    EvalRun(
        name="Retrieval failure",
        retrieved_ids=["meal-policy", "baggage-policy", "refund-policy"],
        answer="Generation is not scored in this isolated retrieval test.",
        labels=AnswerLabels(None, None, None),
    ),
    EvalRun(
        name="Generation failure",
        retrieved_ids=["hotel-policy", "meal-policy", "baggage-policy"],
        answer="Yes. A six-hour delay qualifies for a free hotel.",
        labels=AnswerLabels(
            faithfulness=False,
            answer_relevance=True,
            correctness=False,
        ),
    ),
    EvalRun(
        name="Passing run",
        retrieved_ids=["hotel-policy", "meal-policy", "baggage-policy"],
        answer=(
            "A six-hour delay alone does not establish eligibility. The delay must "
            "require an overnight stay and be caused by the airline."
        ),
        labels=AnswerLabels(
            faithfulness=True,
            answer_relevance=True,
            correctness=True,
        ),
    ),
]


if __name__ == "__main__":
    print(f"Question: {QUESTION}")
    print(f"Gold policy: {GOLD_POLICY}")
    for eval_run in runs:
        print(f"  Diagnosis: {diagnose(eval_run)}")
