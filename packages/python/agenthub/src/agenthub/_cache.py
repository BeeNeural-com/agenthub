"""Local fetch cache for Agent Hub resources — lock file + on-disk entries."""
from __future__ import annotations

import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

from agenthub._loader import Resource, read_resource_file

LOCKFILE_VERSION = 1
LOCKFILE_NAME = "agenthub-cache-lock.json"
CACHE_PATH_ENV = "AGENTHUB_CACHE_PATH"


def discover_cache_path(catalog_root: Path | None = None) -> Path:
    """Resolve cache directory from AGENTHUB_CACHE_PATH or catalog default."""
    env = os.environ.get(CACHE_PATH_ENV)
    if env and env.strip():
        return Path(env.strip()).resolve()
    if catalog_root is not None:
        return (catalog_root.resolve() / ".agenthub-cache").resolve()
    return (Path.home() / ".agenthub-cache").resolve()


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _entry_rel_path(resource_type: str, resource_id: str, suffix: str) -> str:
    return f"{resource_type}/{resource_id}/{suffix}".replace("\\", "/")


class ResourceCache:
    """Disk cache for resource bodies and supporting files, tracked by a lock file."""

    def __init__(self, catalog_root: Path | None = None, cache_path: Path | None = None) -> None:
        self.cache_path = (cache_path or discover_cache_path(catalog_root)).resolve()
        self.lock_path = self.cache_path / LOCKFILE_NAME
        self.cache_path.mkdir(parents=True, exist_ok=True)
        self._lock = self._load_lock()

    def _load_lock(self) -> dict:
        if not self.lock_path.is_file():
            return self._empty_lock()
        try:
            data = json.loads(self.lock_path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return self._empty_lock()
            entries = data.get("entries")
            if not isinstance(entries, list):
                data["entries"] = []
            return data
        except (OSError, ValueError):
            return self._empty_lock()

    def _empty_lock(self) -> dict:
        return {
            "lockfileVersion": LOCKFILE_VERSION,
            "generatedAt": _utc_now_iso(),
            "cachePath": str(self.cache_path),
            "entries": [],
        }

    def _save_lock(self) -> None:
        self._lock["generatedAt"] = _utc_now_iso()
        self._lock["cachePath"] = str(self.cache_path)
        self.lock_path.write_text(json.dumps(self._lock, indent=2) + "\n", encoding="utf-8")

    def _find_entry(self, resource_type: str, resource_id: str) -> dict | None:
        for entry in self._lock.get("entries", []):
            if not isinstance(entry, dict):
                continue
            if entry.get("type") == resource_type and entry.get("id") == resource_id:
                return entry
        return None

    def _upsert_entry(
        self,
        resource_type: str,
        resource_id: str,
        version: str,
        body_rel: str,
        files: list[str],
    ) -> None:
        entries = self._lock.setdefault("entries", [])
        now = _utc_now_iso()
        existing = self._find_entry(resource_type, resource_id)
        payload = {
            "id": resource_id,
            "type": resource_type,
            "version": version,
            "cachedAt": now,
            "path": body_rel,
            "files": sorted(files),
        }
        if existing is None:
            entries.append(payload)
        else:
            existing.update(payload)

    def get_body(self, resource_type: str, resource_id: str, version: str) -> str | None:
        entry = self._find_entry(resource_type, resource_id)
        if entry is None or entry.get("version") != version:
            return None
        rel = entry.get("path")
        if not isinstance(rel, str):
            return None
        target = (self.cache_path / rel).resolve()
        if not target.is_relative_to(self.cache_path.resolve()) or not target.is_file():
            return None
        return target.read_text(encoding="utf-8")

    def put_body(
        self,
        resource_type: str,
        resource_id: str,
        version: str,
        body: str,
        files: list[str] | None = None,
    ) -> None:
        body_rel = _entry_rel_path(resource_type, resource_id, "body.md")
        target = self.cache_path / body_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding="utf-8")
        self._upsert_entry(resource_type, resource_id, version, body_rel, files or [])
        self._save_lock()

    def get_file(
        self,
        resource_type: str,
        resource_id: str,
        path: str,
        version: str,
    ) -> str | None:
        entry = self._find_entry(resource_type, resource_id)
        if entry is None or entry.get("version") != version:
            return None
        normalized = path.replace("\\", "/")
        cached_files = entry.get("files") or []
        if normalized not in [str(f).replace("\\", "/") for f in cached_files]:
            return None
        rel = _entry_rel_path(resource_type, resource_id, f"files/{normalized}")
        target = (self.cache_path / rel).resolve()
        if not target.is_relative_to(self.cache_path.resolve()) or not target.is_file():
            return None
        return target.read_text(encoding="utf-8")

    def put_file(
        self,
        resource_type: str,
        resource_id: str,
        path: str,
        version: str,
        content: str,
        *,
        files: list[str] | None = None,
    ) -> None:
        normalized = path.replace("\\", "/")
        rel = _entry_rel_path(resource_type, resource_id, f"files/{normalized}")
        target = self.cache_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        entry = self._find_entry(resource_type, resource_id)
        known_files = list(files or [])
        if entry and isinstance(entry.get("files"), list):
            for item in entry["files"]:
                if isinstance(item, str) and item not in known_files:
                    known_files.append(item)
        if normalized not in known_files:
            known_files.append(normalized)
        body_rel = _entry_rel_path(resource_type, resource_id, "body.md")
        if entry and isinstance(entry.get("path"), str):
            body_rel = entry["path"]
        self._upsert_entry(resource_type, resource_id, version, body_rel, known_files)
        self._save_lock()

    def get_or_fetch_body(self, resource: Resource) -> str:
        cached = self.get_body(resource.resource_type, resource.id, resource.version)
        if cached is not None:
            return cached
        self.put_body(
            resource.resource_type,
            resource.id,
            resource.version,
            resource.body,
            resource.files,
        )
        return resource.body

    def get_or_fetch_file(self, resource: Resource, path: str) -> str | None:
        cached = self.get_file(resource.resource_type, resource.id, path, resource.version)
        if cached is not None:
            return cached
        content = read_resource_file(resource, path)
        if content is None:
            return None
        self.put_file(
            resource.resource_type,
            resource.id,
            path,
            resource.version,
            content,
            files=resource.files,
        )
        return content

    def clear(self) -> None:
        if self.cache_path.is_dir():
            shutil.rmtree(self.cache_path)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        self._lock = self._empty_lock()
        self._save_lock()

    def status(self) -> dict:
        entries = self._lock.get("entries", [])
        return {
            "cachePath": str(self.cache_path),
            "lockfileVersion": self._lock.get("lockfileVersion", LOCKFILE_VERSION),
            "generatedAt": self._lock.get("generatedAt"),
            "entryCount": len(entries) if isinstance(entries, list) else 0,
            "entries": entries if isinstance(entries, list) else [],
        }
