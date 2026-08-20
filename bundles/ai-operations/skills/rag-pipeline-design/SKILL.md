---
name: rag-pipeline-design
description: >-
  Design retrieval-augmented generation pipelines: ingestion, chunking, retrieval, reranking. Use for knowledge-base Q&A features.
tags: [ai-operations, rag]
---

# RAG Pipeline Design

## When to Use

- Building internal doc search + Q&A
- Improving RAG accuracy or hallucination rate
- Adding new document sources to existing RAG

## Procedure

### Step 1: Source inventory

- List document types, update frequency, access control
- Define metadata fields for filtering
- Plan PII redaction before indexing

### Step 2: Chunking strategy

- Chunk size vs context window tradeoff
- Overlap for continuity; respect section boundaries
- Store chunk provenance for citations

### Step 3: Retrieval stack

- Embedding model and vector index choice
- Hybrid search: semantic + keyword if needed
- Reranker for top-k precision

### Step 4: Generation guardrails

- Require citations from retrieved chunks
- Fallback when retrieval confidence low
- Monitor via **llm-risk-review** checklist

## Output

Architecture doc at `doc/ai/rag-<product>.md`.
