"""Small, inspectable Markdown chunker for the chunking lesson."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    section: str
    text: str
    source_id: str
    version: str
    access: str


def split_markdown_sections(
    text: str,
    *,
    source_id: str,
    version: str,
    access: str,
) -> list[Chunk]:
    """Split Markdown at level-two headings and retain retrieval metadata."""
    chunks: list[Chunk] = []
    heading = "Document"
    body: list[str] = []

    def save_section() -> None:
        section_text = "\n".join(body).strip()
        if not section_text:
            return
        chunks.append(
            Chunk(
                section=heading,
                text=f"{heading}\n{section_text}",
                source_id=source_id,
                version=version,
                access=access,
            )
        )

    for line in text.splitlines():
        if line.startswith("## "):
            save_section()
            heading = line.removeprefix("## ").strip()
            body = []
        else:
            body.append(line)

    save_section()
    return chunks


POLICY = """\
## Hotel accommodation

We provide a hotel only when the delay requires an overnight stay
and the disruption was caused by the airline.

## Meal vouchers

We provide a meal voucher after a delay of three hours.
"""


if __name__ == "__main__":
    policy_chunks = split_markdown_sections(
        POLICY,
        source_id="passenger-care-policy",
        version="2026-07",
        access="public",
    )

    assert len(policy_chunks) == 2
    assert policy_chunks[0].section == "Hotel accommodation"
    assert "overnight stay" in policy_chunks[0].text
    assert "caused by the airline" in policy_chunks[0].text
    assert "Meal vouchers" not in policy_chunks[0].text

    for policy_chunk in policy_chunks:
        print(policy_chunk)
