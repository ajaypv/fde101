"""Keep retrieval scores separate from answer-quality judgments."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class EvalCase:
    question: str
    relevant_passage_ids: set[str]
    reference_answer: str


@dataclass(frozen=True)
class RagRun:
    retrieved_passage_ids: list[str]
    context: str
    answer: str


@dataclass(frozen=True)
class AnswerGrades:
    grounded: bool
    relevant: bool
    correct: bool


class AnswerGrader(Protocol):
    def grade(self, case: EvalCase, run: RagRun) -> AnswerGrades: ...


def evaluate_rag_run(
    case: EvalCase, run: RagRun, *, k: int, grader: AnswerGrader
) -> dict[str, float | bool | None]:
    if k <= 0 or len(run.retrieved_passage_ids) < k:
        raise ValueError("k must be positive and no larger than the result list")

    top_k = run.retrieved_passage_ids[:k]
    relevant_found = sum(item in case.relevant_passage_ids for item in top_k)
    grades = grader.grade(case, run)
    recall = (
        relevant_found / len(case.relevant_passage_ids)
        if case.relevant_passage_ids
        else None
    )

    return {
        "precision_at_k": relevant_found / k,
        # Recall is undefined when the case has no labeled relevant passages.
        "recall_at_k": recall,
        "grounded": grades.grounded,
        "answer_relevant": grades.relevant,
        "correct": grades.correct,
    }
