---
title: Graph database
description: A database that represents entities as nodes and explicit connections as relationships.
contentType: glossary
level: Beginner
minutes: 4
topics: [graph database, nodes, relationships, traversal]
lastVerified: 2026-08-15
sources:
  - title: Graph database concepts
    url: https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/
    publisher: Neo4j
    type: official-doc
---

A **graph database** stores and queries connected data. In a property graph, domain entities are nodes, explicit connections are relationships, and both can hold properties.

## Tiny example

```text
(Asha:Person)-[:WORKED_AT]->(Acme:Company)
(Asha)-[:KNOWS]->(Maya:Person)
```

A traversal can follow `KNOWS` from Maya to Asha or `WORKED_AT` from Asha to Acme. The result depends on stored edges and the rules of the query.

## Graph search versus vector search

- Graph traversal answers questions about explicit connectivity: “Who worked with Maya?”
- Vector search ranks learned similarity: “Whose profile resembles this role description?”
- Structured filters enforce exact constraints: “Only profiles available in India.”

The graph inside an HNSW vector index is different. HNSW edges help the index navigate between nearby vectors; they do not represent business relationships.

See the complete [vector search or graph search lesson](../../rag/vector-vs-graph-search/).
