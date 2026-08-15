"""Transparent retrieval metrics with explicit denominators."""


def validate_k(retrieved: list[str], k: int) -> None:
    if k <= 0:
        raise ValueError("k must be positive")
    if len(retrieved) < k:
        raise ValueError("retrieved must contain at least k results")


def precision_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    validate_k(retrieved, k)
    top_k = retrieved[:k]
    relevant_retrieved = sum(document_id in relevant for document_id in top_k)
    return relevant_retrieved / k


def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    validate_k(retrieved, k)
    if not relevant:
        return 0.0
    relevant_retrieved = sum(document_id in relevant for document_id in retrieved[:k])
    return relevant_retrieved / len(relevant)


retrieved_ids = ["refund-policy", "pricing", "security"]
relevant_ids = {"refund-policy", "cancellation-policy"}

print(precision_at_k(retrieved_ids, relevant_ids, k=3))  # 1 / 3
print(recall_at_k(retrieved_ids, relevant_ids, k=3))     # 1 / 2
