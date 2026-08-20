---
name: 'Python Guidelines'
description: 'Coding conventions for Python files'
---

# GitHub Copilot Instructions — Python Coding Standard

This file defines the Python coding standard for this repository. Apply these rules to all generated and suggested Python code.

---

## Language & Runtime

- Target **Python 3.10+**. Use modern syntax: `X | Y` unions, `match`/`case`, built-in generics (`list[str]`, `dict[str, int]` — not `List`, `Dict` from `typing`).
- Add `from __future__ import annotations` at the top of every module that uses forward references or self-referential types.

---

## Type Hints

Every function and method — including `__init__` — must have complete type annotations on **all** parameters and the return type.

```python
# Wrong
def build_catalog(repo_path, settings=None):
    ...

# Correct
def build_catalog(
    repo_path: Path | str,
    settings: RegistrySettings | None = None,
) -> Catalog:
    ...
```

- Use `X | None` over `Optional[X]`.
- Use `X | Y` over `Union[X, Y]`.
- Use `collections.abc` types for abstract collections (`Sequence`, `Mapping`, `Callable`, `Iterator`).
- Prefer `TypeAlias` for complex type definitions; use `TypeVar` and `Generic` for reusable generic types.
- Mark read-only collection parameters as `Sequence[T]` or `Mapping[K, V]`, not `list` or `dict`.

---

## Docstrings

All **public** functions, classes, and methods (no leading underscore) must have a **Google-style** docstring.

```python
def scan_entry(
    repo: Repo,
    root: Path,
    file_path: Path,
    resource_type: ResourceType,
) -> CatalogEntry:
    """Build a single CatalogEntry for the given file.

    Reads the file, parses its YAML frontmatter, derives the slug from the
    repository-relative path, and fetches git history via GitPython.

    Args:
        repo: Open GitPython repository instance.
        root: Absolute path to the repository root.
        file_path: Absolute path to the resource file to scan.
        resource_type: The resource type to assign this entry.

    Returns:
        A fully-populated CatalogEntry with metadata, content, and git info.

    Raises:
        FileNotFoundError: If file_path does not exist.
        InvalidGitRepositoryError: If root is not inside a git repository.
    """
```

- **Summary line**: one sentence, imperative mood, ends with a period.
- **Args**: one entry per parameter — `name: Description.`
- **Returns**: what is returned and its meaning (omit for `None`).
- **Raises**: every exception the function can raise intentionally.
- **Example**: include for non-trivial public functions.
- One-liners are acceptable for simple, self-evident functions.
- Private functions (`_name`) should have docstrings when the logic is non-obvious.

---

## Error Handling

Never use bare `except:` or silent `except Exception: pass`.

```python
# Wrong — swallows all errors including KeyboardInterrupt
try:
    result = process()
except:
    pass

# Wrong — hides bugs
try:
    result = process()
except Exception:
    pass

# Correct — catch specific exceptions
try:
    result = process()
except ValueError as e:
    logger.warning("Invalid input: %s", e)
    raise

# Correct — use contextlib.suppress only for truly ignorable errors
import contextlib
with contextlib.suppress(FileNotFoundError):
    cache_file.unlink()

# Correct — chain exceptions in except blocks
try:
    raw = settings.fetch_remote_catalog()
except urllib.error.URLError as exc:
    raise CatalogFetchError("Failed to fetch remote catalog") from exc
```

- Always use `raise ... from exc` when re-raising inside an `except` block.
- Use `contextlib.suppress(SpecificError)` instead of `try/except/pass`.
- Define custom exception classes for domain-specific errors.

---

## Logging

Never use `print()` in application code. Use the `logging` module.

```python
# Wrong
print(f"Processing order {order_id}")
print("ERROR: Payment failed:", exc)

# Correct
import logging
logger = logging.getLogger(__name__)   # module-level, named after the module

logger.info("Processing order %s", order_id)
logger.error("Payment failed", exc_info=True, extra={"order_id": order_id})
```

- Use `%s` lazy formatting in log calls — never f-strings (the string is formatted only if the message is emitted).
- Use `exc_info=True` on `ERROR` and `CRITICAL` for unexpected exceptions.
- Never log secrets, passwords, tokens, or PII.
- `print()` is only acceptable for CLI output explicitly intended for stdout (e.g., `--output` results piped to another tool).

---

## Code Structure & Design

### Functions
- Functions do one thing. If you need "and" to describe it, split it.
- Keep function bodies under ~20 lines of logic. Extract helpers otherwise.
- No magic numbers or strings — use named constants or `Enum`.
- Use `pathlib.Path` over `os.path` for all file system operations.
- Use `contextlib` context managers for resource acquisition/release.

### Classes
- Apply SOLID principles: single responsibility, open/closed, dependency inversion.
- Prefer composition over inheritance.
- Use `@dataclass` or Pydantic `BaseModel` for data containers — not bare `__init__` with many attributes.
- Use `@dataclass(frozen=True)` for immutable value objects.
- Use `abc.ABC` + `@abstractmethod` to define contracts/interfaces.

### Imports
Imports must be grouped and ordered (enforced by ruff/isort):

```python
# 1. stdlib
from __future__ import annotations

import contextlib
import hashlib
from pathlib import Path
from typing import TYPE_CHECKING

# 2. third-party
from pydantic import BaseModel, Field

# 3. first-party
from agent_registry.models import Catalog, ResourceType

# TYPE_CHECKING block at the end (avoids circular imports at runtime)
if TYPE_CHECKING:
    from agent_registry.settings import RegistrySettings
```

---

## Data Models — Pydantic v2

Use Pydantic `BaseModel` for all structured data. Apply v2 patterns:

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Self, Annotated

class ResourceMeta(BaseModel):
    name: str = Field(..., min_length=1)
    version: str = Field(default="0.1.0")
    tags: list[str] = Field(default_factory=list)   # never default=[]

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        return v.strip()

    @model_validator(mode="after")
    def normalize(self) -> Self:
        self.tags = sorted(set(t.lower() for t in self.tags))
        return self
```

- Use `default_factory=list` / `default_factory=dict` — never bare `[]` or `{}` as defaults.
- Use `SecretStr` for any sensitive field.
- Use `model_dump(exclude_unset=True)` in PATCH handlers.
- Set `extra="forbid"` on input-facing models to catch unexpected fields early.
- Use `pydantic-settings` + `BaseSettings` for application configuration.

---

## Testing

- All tests use **pytest**. No `unittest.TestCase` subclasses.
- Minimum **80% coverage** on `src/` — enforced by CI (`--cov-fail-under=80`).
- Use `tmp_path` for any file system interaction in tests.
- Mock external dependencies (`git`, `urllib`, filesystem) — no network calls in tests.
- Group related tests in classes: `class TestSlugify:`.
- Test names describe behaviour: `test_returns_empty_string_for_empty_input`.

```python
class TestContentHash:
    def test_deterministic_for_same_input(self) -> None:
        assert _content_hash(b"hello") == _content_hash(b"hello")

    def test_differs_for_different_input(self) -> None:
        assert _content_hash(b"hello") != _content_hash(b"world")

    def test_empty_bytes_returns_valid_hex(self) -> None:
        result = _content_hash(b"")
        assert len(result) == 64
        assert all(c in "0123456789abcdef" for c in result)
```

---

## Formatting & Linting (Ruff)

All code must pass `ruff check` and `ruff format` with this project's configuration:

| Setting | Value |
|---------|-------|
| Line length | 100 characters |
| Quote style | Double quotes |
| Indent | 4 spaces |
| Target | Python 3.10 |

Run before committing:
```bash
uv run ruff format src/ tests/
uv run ruff check src/ tests/
```

Active rule sets: `E/W` (pycodestyle), `F` (pyflakes), `I` (isort), `B` (bugbear), `UP` (pyupgrade), `N` (naming), `SIM` (simplify), `RUF` (ruff-specific).

---

## Commit Messages

Follow **Conventional Commits**:

```
<type>(<scope>): <short summary>

[optional body]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`

```
feat(scanner): add recursive subdirectory support
fix(generator): escape HTML in resource names
refactor(cli): extract _source helper from show_config
test(scanner): add edge cases for missing frontmatter
```

- Summary line: imperative mood, lowercase, no trailing period, max 72 characters.
- Body: explain *why*, not *what* (the diff shows what).
