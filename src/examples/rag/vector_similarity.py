"""A dependency-free cosine similarity and exact-search example."""

from math import sqrt
from typing import Iterable, Sequence


Vector = Sequence[float]


def cosine_similarity(left: Vector, right: Vector) -> float:
    """Return the normalized dot product of two non-zero vectors."""
    if len(left) != len(right):
        raise ValueError("vectors must have the same dimensions")

    dot_product = sum(a * b for a, b in zip(left, right))
    left_length = sqrt(sum(value * value for value in left))
    right_length = sqrt(sum(value * value for value in right))
    if left_length == 0 or right_length == 0:
        raise ValueError("cosine similarity is undefined for a zero vector")

    return dot_product / (left_length * right_length)


def exact_search(
    query: Vector,
    documents: Iterable[tuple[str, Vector]],
    *,
    k: int,
) -> list[tuple[str, float]]:
    """Score every document, then return the k highest scores."""
    scored = [
        (document_id, cosine_similarity(query, vector))
        for document_id, vector in documents
    ]
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]


if __name__ == "__main__":
    query_vector = [1.0, 0.0]
    document_vectors = [
        ("password-reset", [0.9, 0.1]),
        ("account-lockout", [0.7, 0.3]),
        ("office-map", [0.0, 1.0]),
    ]

    for name, score in exact_search(query_vector, document_vectors, k=3):
        print(f"{name:18} cosine={score:.3f}")
