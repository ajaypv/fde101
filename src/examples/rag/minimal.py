"""A provider-neutral RAG pipeline small enough to read in one sitting."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Passage:
    text: str
    source: str


class Retriever(Protocol):
    def search(self, query: str, *, k: int) -> list[Passage]: ...


class LanguageModel(Protocol):
    def generate(self, prompt: str) -> str: ...


def answer_with_rag(
    question: str,
    *,
    retriever: Retriever,
    model: LanguageModel,
) -> str:
    passages = retriever.search(question, k=4)
    context = "\n\n".join(
        f"[{index}] {passage.text}\nSource: {passage.source}"
        for index, passage in enumerate(passages, start=1)
    )

    prompt = f"""Answer using only the context below.
If the context is insufficient, say you do not know.
Cite supporting passages with [1], [2], and so on.

Context:
{context}

Question: {question}
Answer:"""

    return model.generate(prompt)
