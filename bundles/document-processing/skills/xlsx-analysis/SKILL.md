---
name: xlsx-analysis
description: >-
  Build and analyze Excel spreadsheets with formulas, pivot tables, and charts. Use for financial models, operational dashboards, and data summaries.
tags: [document-processing, xlsx]
---

# XLSX Analysis

## When to Use

- Analyzing tabular data with formulas or pivots
- Building a reusable spreadsheet template for a team
- Validating imported CSV data before downstream use

## Procedure

### Step 1: Define the model

- Separate inputs (assumptions), calculations, and outputs on distinct sheets
- Document units and source of each assumption cell
- Use named ranges for key inputs referenced across sheets

### Step 2: Build calculations

- Prefer structured references (Excel tables) over loose ranges
- Avoid hard-coded constants in formulas — reference assumption cells
- Add data validation for dropdown inputs where applicable

### Step 3: Visualize and summarize

- Choose chart types that match the message (trend vs composition)
- Add pivot tables for slice-and-dice exploration
- Include a summary dashboard sheet with KPI callouts

### Step 4: Validate

- Spot-check formulas with edge cases (zero, negative, null)
- Compare totals against source system exports
- Lock formula cells and protect structure before sharing

## Output

Deliver `doc/analysis/<topic>.xlsx` plus a one-page interpretation in markdown.
