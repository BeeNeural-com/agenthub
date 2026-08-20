---
description: Grammar and writing quality rules for all project text — AsciiDoc documents, C++ Doxygen comment blocks, and Markdown files.
applyTo: "**/*"
---

# Grammar and Writing Quality Rules

These rules apply to every text artifact in this project: AsciiDoc requirements and architecture documents, C++ Doxygen comment blocks, Markdown agent and instruction files, and any other prose.

---

## Em-Dash Prohibition

Do not use em dashes (`—`) in normative prose, comments, or documentation strings. Em dashes create reading ambiguity in formal specifications.

Use instead:
- Commas for parenthetical asides
- Semicolons for related independent clauses
- Colons before elaborating clauses
- Parentheses for supplementary information that does not change the meaning

The pattern `Field: N/A — <reason>` is a recurring violation. Replace with `Field: N/A: <reason>` (colon introduces the elaborating clause).

## Headings (Markdown)

- Use sentence case: capitalize only the first word and proper nouns.
- No special characters in headings: avoid `@#$%^&*[]{}<>+.'"\|/``~_`.

## Sentence Structure

- Write in short, declarative sentences. One idea per sentence.
- Prefer active voice. Write "The server closes the connection", not "The connection is closed by the server."
- Do not start a sentence with "Note that", "Please note", or "It should be noted". State the fact directly.
- Avoid filler phrases: "In order to" becomes "To"; "Due to the fact that" becomes "Because"; "At this point in time" becomes "Now" or "Currently".

## Abbreviations and Acronyms

- Expand abbreviations on first use in every document section: write the full term followed by the abbreviation in parentheses.
- Do not introduce new abbreviations for terms that appear fewer than three times in the section.

## Self-Check

- [ ] No em dashes (`—`) anywhere in the text
- [ ] Sentences are short and declarative
- [ ] Active voice used throughout
- [ ] No filler phrases ("in order to", "it should be noted", "at this point in time")
- [ ] Abbreviations expanded on first use
