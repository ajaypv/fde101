"""Turn one Markdown section into a parent and searchable child records."""

from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class MarkdownSection:
    heading_path: tuple[str, ...]
    blocks: tuple[str, ...]


@dataclass(frozen=True)
class ParentRecord:
    parent_id: str
    heading_path: tuple[str, ...]
    text: str


@dataclass(frozen=True)
class ChildRecord:
    chunk_id: str
    parent_id: str
    kind: str
    heading_path: tuple[str, ...]
    text: str


def group_markdown_blocks(lines: list[str]) -> tuple[str, ...]:
    """Group blank-line-separated Markdown without breaking a table."""
    blocks: list[str] = []
    current: list[str] = []

    def save_block() -> None:
        text = "\n".join(current).strip()
        if text:
            blocks.append(text)

    for line in lines:
        if line.strip():
            current.append(line)
        else:
            save_block()
            current = []

    save_block()
    return tuple(blocks)


def split_markdown_sections(markdown: str) -> list[MarkdownSection]:
    """Split at level-two headings and retain the document heading path."""
    document_title = "Document"
    section_title: str | None = None
    section_lines: list[str] = []
    sections: list[MarkdownSection] = []

    def save_section() -> None:
        if section_title is None:
            return
        blocks = group_markdown_blocks(section_lines)
        if blocks:
            sections.append(
                MarkdownSection(
                    heading_path=(document_title, section_title),
                    blocks=blocks,
                )
            )

    for line in markdown.splitlines():
        if line.startswith("# "):
            document_title = line.removeprefix("# ").strip()
        elif line.startswith("## "):
            save_section()
            section_title = line.removeprefix("## ").strip()
            section_lines = []
        elif section_title is not None:
            section_lines.append(line)

    save_section()
    return sections


def slug(text: str) -> str:
    """Create a stable, readable identifier fragment for this example."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def block_kind(block: str) -> str:
    """Label a Markdown table separately from ordinary prose."""
    lines = block.splitlines()
    if len(lines) >= 2 and lines[0].lstrip().startswith("|"):
        return "table"
    return "paragraph"


def create_parent_child_records(
    section: MarkdownSection,
    *,
    document_id: str,
    version: str,
) -> tuple[ParentRecord, list[ChildRecord]]:
    """Keep the full section as a parent and each block as a search child."""
    section_slug = slug(section.heading_path[-1])
    parent_id = f"{document_id}:v{version}:{section_slug}"
    heading = " > ".join(section.heading_path)
    parent = ParentRecord(
        parent_id=parent_id,
        heading_path=section.heading_path,
        text=f"{heading}\n\n" + "\n\n".join(section.blocks),
    )

    children = [
        ChildRecord(
            chunk_id=f"{parent_id}:child-{position:02d}",
            parent_id=parent_id,
            kind=block_kind(block),
            heading_path=section.heading_path,
            text=f"{heading}\n\n{block}",
        )
        for position, block in enumerate(section.blocks, start=1)
    ]
    return parent, children


POLICY_MARKDOWN = """\
# Irregular Operations Policy

## Hotel accommodation

A hotel is provided only when the delay requires an overnight stay
and the disruption was caused by the airline.

| Delay condition | Hotel eligibility |
| --- | --- |
| Overnight and airline-controlled | Eligible |
| Weather disruption | Not automatically eligible |
"""


if __name__ == "__main__":
    policy_sections = split_markdown_sections(POLICY_MARKDOWN)
    assert len(policy_sections) == 1

    policy_parent, policy_children = create_parent_child_records(
        policy_sections[0],
        document_id="IRROPS-204",
        version="3",
    )

    assert len(policy_children) == 2
    assert policy_children[0].kind == "paragraph"
    assert "overnight stay" in policy_children[0].text
    assert "caused by the airline" in policy_children[0].text
    assert policy_children[1].kind == "table"
    assert "| Delay condition | Hotel eligibility |" in policy_children[1].text
    assert all(child.parent_id == policy_parent.parent_id for child in policy_children)

    print(policy_parent)
    for policy_child in policy_children:
        print(policy_child)
