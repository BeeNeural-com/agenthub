---
name: pdf-extraction
description: >-
  Extract text, tables, and metadata from PDFs and merge or split documents. Use when ingesting contracts, invoices, or research papers.
tags: [document-processing, pdf]
---

# PDF Extraction

## When to Use

- Pulling tables or text from scanned or digital PDFs
- Merging multiple PDFs into a single deliverable
- Preparing PDF content for search or summarization

## Procedure

### Step 1: Assess PDF type

- Determine if text is selectable (digital) or requires OCR
- Note page count, encryption, and form fields
- Identify tables vs free text vs images

### Step 2: Extract content

- Extract text preserving heading structure where possible
- For tables, export to CSV/XLSX and validate row/column counts
- Capture metadata: title, author, creation date

### Step 3: Clean and structure

- Remove headers/footers and page numbers from body text
- Fix hyphenation and line-break artifacts from OCR
- Tag sections for downstream search or RAG chunking

### Step 4: Merge or split (if needed)

- Define page ranges for split outputs
- Add bookmarks for merged documents
- Verify file size and accessibility of output PDFs

## Output

Save extracted content under `doc/extracts/<source>-extract.md` and tables as CSV.
