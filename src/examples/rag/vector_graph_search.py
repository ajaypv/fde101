"""Compare lexical, vector, filter, and graph retrieval without dependencies."""

from dataclasses import dataclass
from math import sqrt


Vector = tuple[float, ...]


@dataclass(frozen=True)
class Profile:
    summary: str
    skills: frozenset[str]
    region: str
    available: bool
    embedding: Vector


# These three-dimensional vectors are hand-written teaching data. A real system
# would pin an embedding model and create vectors from the query and profiles.
PROFILES = {
    "Asha": Profile(
        summary="Built ETL workflows with PySpark on Google Cloud.",
        skills=frozenset({"python", "pyspark", "gcp", "etl"}),
        region="India",
        available=True,
        embedding=(0.90, 0.80, 0.75),
    ),
    "Ben": Profile(
        summary="Developed Python API services on AWS.",
        skills=frozenset({"python", "fastapi", "aws"}),
        region="India",
        available=True,
        embedding=(0.95, 0.75, 0.10),
    ),
    "Chen": Profile(
        summary="Designed Spark pipelines and a warehouse on Azure.",
        skills=frozenset({"spark", "azure", "data-engineering"}),
        region="India",
        available=True,
        embedding=(0.25, 0.80, 0.90),
    ),
    "Dina": Profile(
        summary="Built Python batch jobs on GCP for analytics.",
        skills=frozenset({"python", "gcp", "data-engineering"}),
        region="India",
        available=False,
        embedding=(0.90, 0.65, 0.85),
    ),
}

# These typed edges are product-domain facts. They are not HNSW edges.
RELATIONSHIPS = {
    "you": {("KNOWS", "Maya"), ("KNOWS", "Ravi")},
    "Maya": {("KNOWS", "you"), ("WORKED_WITH", "Asha")},
    "Ravi": {("KNOWS", "you"), ("KNOWS", "Noor")},
    "Noor": {("KNOWS", "Ravi")},
    "Asha": {("WORKED_WITH", "Maya")},
    "Ben": set(),
    "Chen": set(),
    "Dina": set(),
}


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


def lexical_matches(term: str) -> list[str]:
    """Find an exact text term after case normalization."""
    needle = term.casefold()
    return [
        name for name, profile in PROFILES.items()
        if needle in profile.summary.casefold()
    ]


def semantic_ranking(query: Vector, names: list[str]) -> list[tuple[str, float]]:
    """Rank candidates by cosine similarity to the teaching query vector."""
    scored = [
        (name, cosine_similarity(query, PROFILES[name].embedding))
        for name in names
    ]
    return sorted(scored, key=lambda item: item[1], reverse=True)


def follows_typed_path(
    start: str,
    target: str,
    relationship_types: tuple[str, ...],
) -> bool:
    """Return whether an exact sequence of relationship types reaches target."""
    frontier = {start}
    for relationship_type in relationship_types:
        frontier = {
            neighbor
            for node in frontier
            for edge_type, neighbor in RELATIONSHIPS.get(node, set())
            if edge_type == relationship_type
        }
    return target in frontier


if __name__ == "__main__":
    query_vector = (1.0, 1.0, 1.0)  # Python + cloud + data engineering

    print("Lexical match for 'GCP':", lexical_matches("GCP"))

    print("\nSemantic ranking (no hard constraints):")
    for name, score in semantic_ranking(query_vector, list(PROFILES)):
        print(f"  {name:5} cosine={score:.3f}")

    # Exact product constraints do not belong inside an embedding score.
    eligible = [
        name
        for name, profile in PROFILES.items()
        if profile.available
        and profile.region == "India"
        and "python" in profile.skills
    ]

    required_path = ("KNOWS", "WORKED_WITH")
    print("\nHybrid result (eligible and matched KNOWS -> WORKED_WITH):")
    for name, score in semantic_ranking(query_vector, eligible):
        if follows_typed_path("you", name, required_path):
            print(f"  {name:5} cosine={score:.3f} path={' -> '.join(required_path)}")
