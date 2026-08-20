"""Resolve remote catalog sources (GitHub) without requiring a full user clone."""
from __future__ import annotations

import os
import re
import shutil
import tempfile
import urllib.error
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path

DEFAULT_GITHUB_OWNER = "BeeNeural-com"
DEFAULT_GITHUB_REPO = "agenthub"
DEFAULT_GITHUB_REF = "main"
DEFAULT_SOURCE = f"github:{DEFAULT_GITHUB_OWNER}/{DEFAULT_GITHUB_REPO}@{DEFAULT_GITHUB_REF}"

CATALOG_SOURCE_ENV = "AGENTHUB_CATALOG_SOURCE"
CATALOG_URL_ENV = "AGENTHUB_CATALOG_URL"
GITHUB_TOKEN_ENVS = ("AGENTHUB_GITHUB_TOKEN", "GITHUB_TOKEN")

# github:owner/repo[@ref]
_GITHUB_SHORTHAND = re.compile(
    r"^github:(?P<owner>[^/\s]+)/(?P<repo>[^/@\s]+)(?:@(?P<ref>[^\s]+))?$",
    re.IGNORECASE,
)
# https://github.com/owner/repo[.git][/tree/ref|/...]
_GITHUB_HTTPS = re.compile(
    r"^https?://(?:www\.)?github\.com/(?P<owner>[^/\s]+)/(?P<repo>[^/\s#?]+?)(?:\.git)?"
    r"(?:/(?:tree|blob)/(?P<ref>[^/\s#?]+))?/?$",
    re.IGNORECASE,
)
# git+https://... or git@github.com:owner/repo.git
_GITHUB_GIT = re.compile(
    r"^(?:git\+)?(?:https?://(?:www\.)?github\.com/|git@github\.com:)"
    r"(?P<owner>[^/\s]+)/(?P<repo>[^/\s#?]+?)(?:\.git)?(?:@(?P<ref>[^\s#]+))?$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class GitHubRef:
    owner: str
    repo: str
    ref: str = DEFAULT_GITHUB_REF

    @property
    def cache_key(self) -> str:
        safe_ref = re.sub(r"[^\w.\-]+", "_", self.ref)
        return f"{self.owner}__{self.repo}__{safe_ref}"

    def display(self) -> str:
        return f"github:{self.owner}/{self.repo}@{self.ref}"


def github_token() -> str | None:
    for key in GITHUB_TOKEN_ENVS:
        value = os.environ.get(key, "").strip()
        if value:
            return value
    return None


def parse_github_source(source: str) -> GitHubRef | None:
    """Return GitHubRef if *source* is a GitHub URL or github: shorthand; else None."""
    text = source.strip()
    if not text:
        return None

    for pattern in (_GITHUB_SHORTHAND, _GITHUB_HTTPS, _GITHUB_GIT):
        match = pattern.match(text)
        if not match:
            continue
        owner = match.group("owner")
        repo = match.group("repo").removesuffix(".git")
        ref = match.groupdict().get("ref") or DEFAULT_GITHUB_REF
        return GitHubRef(owner=owner, repo=repo, ref=ref)

    # Bare owner/repo (no scheme) — only if it looks like GitHub coords
    if re.fullmatch(r"[^/\s]+/[^/\s@]+(?:@[^\s]+)?", text) and "://" not in text:
        owner_repo, _, ref = text.partition("@")
        owner, _, repo = owner_repo.partition("/")
        if owner and repo:
            return GitHubRef(owner=owner, repo=repo, ref=ref or DEFAULT_GITHUB_REF)

    return None


def is_remote_source(source: str | Path | None) -> bool:
    if source is None:
        return False
    text = str(source).strip()
    if not text:
        return False
    path = Path(text).expanduser()
    # Existing local path wins over shorthand that happens to look like a relative path
    if path.exists():
        return False
    return parse_github_source(text) is not None


def discover_remote_source_string() -> str | None:
    """Env-based remote catalog source (URL or github: shorthand)."""
    for key in (CATALOG_SOURCE_ENV, CATALOG_URL_ENV):
        value = os.environ.get(key, "").strip()
        if value:
            return value
    return None


def _source_cache_root() -> Path:
    override = os.environ.get("AGENTHUB_CACHE_PATH", "").strip()
    if override:
        return Path(override).expanduser().resolve() / "github-sources"
    return (Path.home() / ".agenthub-cache" / "github-sources").resolve()


def _catalog_marker(root: Path) -> bool:
    return (root / "global" / "skills").is_dir()


def _find_catalog_in_extracted(extract_root: Path) -> Path | None:
    """Zipballs nest under owner-repo-<sha>/ — locate global/skills."""
    if _catalog_marker(extract_root):
        return extract_root
    for child in sorted(extract_root.iterdir()):
        if child.is_dir() and _catalog_marker(child):
            return child
    # One more level (rare)
    for child in sorted(extract_root.iterdir()):
        if not child.is_dir():
            continue
        for nested in sorted(child.iterdir()):
            if nested.is_dir() and _catalog_marker(nested):
                return nested
    return None


def _download_zipball(ref: GitHubRef, dest_zip: Path) -> None:
    url = f"https://api.github.com/repos/{ref.owner}/{ref.repo}/zipball/{ref.ref}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "agenthub-cli",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = github_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            dest_zip.write_bytes(response.read())
    except urllib.error.HTTPError as exc:
        hint = ""
        if exc.code in (401, 403, 404):
            hint = (
                " If the repository is private, set GITHUB_TOKEN or AGENTHUB_GITHUB_TOKEN "
                "with repo read access."
            )
        raise RuntimeError(
            f"Failed to download catalog from {ref.display()} ({exc.code} {exc.reason}).{hint}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error downloading {ref.display()}: {exc.reason}") from exc


def _extract_catalog_paths(zip_path: Path, extract_root: Path) -> Path:
    """Extract only global/ and bundles/ from the GitHub zipball."""
    extract_root.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zf:
        members = zf.namelist()
        if not members:
            raise RuntimeError("GitHub zipball is empty")

        # Zip root is typically "Owner-repo-<sha>/"
        top = members[0].split("/")[0]
        wanted_prefixes = (f"{top}/global/", f"{top}/bundles/")

        for name in members:
            if not any(name.startswith(p) for p in wanted_prefixes):
                continue
            # Skip directory entries
            if name.endswith("/"):
                continue
            # Safety: no path traversal
            target = (extract_root / name).resolve()
            if not target.is_relative_to(extract_root.resolve()):
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(name) as src, target.open("wb") as dst:
                shutil.copyfileobj(src, dst)

    catalog = _find_catalog_in_extracted(extract_root)
    if catalog is None:
        raise RuntimeError(
            f"Downloaded archive for {top} does not contain global/skills/. "
            "Confirm the GitHub ref points at an Agent Hub monorepo."
        )
    return catalog


def fetch_github_catalog(
    ref: GitHubRef,
    *,
    cache_dir: Path | None = None,
    force: bool = False,
) -> Path:
    """Download catalog (global/ + bundles/) from GitHub into a local cache directory.

    Returns the path to the catalog root (contains global/ and optionally bundles/).
    """
    root = (cache_dir or _source_cache_root()).resolve()
    dest = root / ref.cache_key
    if not force and _catalog_marker(dest):
        return dest

    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="agenthub-gh-") as tmp:
        tmp_path = Path(tmp)
        zip_path = tmp_path / "catalog.zip"
        extract_root = tmp_path / "extract"
        _download_zipball(ref, zip_path)
        catalog = _extract_catalog_paths(zip_path, extract_root)
        # Move global/ and bundles/ into dest
        for part in ("global", "bundles"):
            src = catalog / part
            if src.is_dir():
                shutil.copytree(src, dest / part, dirs_exist_ok=True)

    if not _catalog_marker(dest):
        raise RuntimeError(f"Failed to materialize catalog at {dest}")
    return dest


def resolve_install_source(source: str | Path | None) -> Path:
    """Resolve install --source to a local catalog root (download if GitHub).

    Accepts:
      - local path
      - https://github.com/BeeNeural-com/agenthub
      - github:BeeNeural-com/agenthub[@ref]
      - None → AGENTHUB_CATALOG_SOURCE / AGENTHUB_CATALOG_URL → else error
    """
    text: str | None
    if source is None:
        text = discover_remote_source_string()
        if text is None:
            # Fall back to AGENTHUB_CATALOG_PATH as local source (existing behavior)
            env_path = os.environ.get("AGENTHUB_CATALOG_PATH", "").strip()
            if env_path:
                return Path(env_path).expanduser().resolve()
            raise FileNotFoundError(
                "No catalog source. Pass --source <path|github-url>, or set "
                f"{CATALOG_SOURCE_ENV} / {CATALOG_URL_ENV} / AGENTHUB_CATALOG_PATH. "
                f"Example: --source {DEFAULT_SOURCE}"
            )
    else:
        text = str(source).strip()

    path = Path(text).expanduser()
    if path.exists():
        return path.resolve()

    gh = parse_github_source(text)
    if gh is not None:
        return fetch_github_catalog(gh)

    # Treat as local path that does not exist yet — clearer error
    raise FileNotFoundError(
        f"Catalog source not found: {text!r}. "
        "Use a local path with global/ + bundles/, or a GitHub URL / "
        f"github:owner/repo (default {DEFAULT_SOURCE})."
    )
