"""A provider-neutral ingestion pipeline with visible production metadata."""

from dataclasses import dataclass
from hashlib import sha256
from typing import Protocol


@dataclass(frozen=True)
class SourceDocument:
    id: str
    title: str
    version: str
    effective_at: str
    source_uri: str
    tenant_id: str
    acl_group_ids: tuple[str, ...]
    markdown: str


@dataclass(frozen=True)
class ChunkRecord:
    chunk_id: str
    document_id: str
    parent_id: str
    section: str
    text: str
    version: str
    effective_at: str
    source_uri: str
    tenant_id: str
    acl_group_ids: tuple[str, ...]
    checksum: str
    embedding: list[float]


class Embedder(Protocol):
    name: str

    def embed_documents(self, texts: list[str]) -> list[list[float]]: ...


class SearchStore(Protocol):
    def remove_old_versions(self, document_id: str, keep_version: str) -> None: ...

    def upsert(self, chunks: list[ChunkRecord]) -> None: ...


def split_sections(markdown: str) -> list[tuple[str, str]]:
    """Keep each level-two heading with the text that belongs to it."""
    sections: list[tuple[str, str]] = []
    heading = "Document"
    body: list[str] = []

    def save() -> None:
        text = "\n".join(body).strip()
        if text:
            sections.append((heading, text))

    for line in markdown.splitlines():
        if line.startswith("## "):
            save()
            heading = line.removeprefix("## ").strip()
            body = []
        else:
            body.append(line)

    save()
    return sections


def ingest_document(
    document: SourceDocument,
    *,
    embedder: Embedder,
    store: SearchStore,
) -> list[ChunkRecord]:
    sections = split_sections(document.markdown)
    searchable_texts = [f"{heading}\n{text}" for heading, text in sections]
    embeddings = embedder.embed_documents(searchable_texts)

    chunks: list[ChunkRecord] = []
    for position, ((heading, text), embedding) in enumerate(
        zip(sections, embeddings, strict=True), start=1
    ):
        searchable_text = f"{heading}\n{text}"
        parent_id = f"{document.id}:{document.version}:{position}"
        chunks.append(
            ChunkRecord(
                chunk_id=f"{parent_id}:child-1",
                document_id=document.id,
                parent_id=parent_id,
                section=heading,
                text=searchable_text,
                version=document.version,
                effective_at=document.effective_at,
                source_uri=document.source_uri,
                tenant_id=document.tenant_id,
                acl_group_ids=document.acl_group_ids,
                checksum=sha256(searchable_text.encode("utf-8")).hexdigest(),
                embedding=embedding,
            )
        )

    # Upsert the current version, then remove versions that must no longer be found.
    store.upsert(chunks)
    store.remove_old_versions(document.id, keep_version=document.version)
    return chunks

