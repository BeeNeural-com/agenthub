"""Core catalog loader — skills, agents, rules, prompts from global/ and bundles/."""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

ENTRY_FILES = {
    "skill": ("SKILL.md",),
    "agent": (".agent.md",),
    "rule": (".instructions.md", ".md"),
    "prompt": (".prompt.md",),
}

RESOURCE_TYPES = ("skill", "agent", "rule", "prompt")
SUBDIRS = {"skill": "skills", "agent": "agents", "rule": "rules", "prompt": "prompts"}


@dataclass
class Resource:
    id: str
    name: str
    description: str
    tags: list[str]
    version: str
    body: str
    folder: Path
    resource_type: str
    source: str
    files: list[str] = field(default_factory=list)


@dataclass
class ResourceMeta:
    id: str
    name: str
    description: str
    tags: list[str]
    version: str
    resource_type: str
    source: str

    @classmethod
    def from_resource(cls, r: Resource) -> ResourceMeta:
        return cls(
            id=r.id,
            name=r.name,
            description=r.description,
            tags=r.tags,
            version=r.version,
            resource_type=r.resource_type,
            source=r.source,
        )


@dataclass
class BundleInfo:
    id: str
    name: str
    description: str
    skill_count: int
    agent_count: int
    rule_count: int
    prompt_count: int


@dataclass
class RagDocument:
    id: str
    text: str
    metadata: dict


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}, text
    return (fm if isinstance(fm, dict) else {}), parts[2].lstrip("\n")


def _read_manifest(folder: Path) -> dict:
    mf = folder / "manifest.yaml"
    if not mf.is_file():
        return {}
    try:
        return yaml.safe_load(mf.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return {}


def _find_entry_file(folder: Path, resource_type: str) -> Path | None:
    for pattern in ENTRY_FILES[resource_type]:
        if pattern.startswith("."):
            for match in sorted(folder.glob(f"*{pattern}")):
                if match.name not in {"manifest.yaml", "README.md"}:
                    return match
        else:
            candidate = folder / pattern
            if candidate.is_file():
                return candidate
    return None


def _collect_supporting_files(folder: Path, entry: Path) -> list[str]:
    return sorted(
        str(p.relative_to(folder)).replace("\\", "/")
        for p in folder.rglob("*")
        if p.is_file() and p != entry and p.name not in {"manifest.yaml", "README.md"}
    )


def load_resources_from_root(root: Path, resource_type: str, source: str) -> dict[str, Resource]:
    resources: dict[str, Resource] = {}
    if not root.is_dir():
        return resources

    for folder in sorted(p for p in root.iterdir() if p.is_dir()):
        entry = _find_entry_file(folder, resource_type)
        if entry is None:
            continue

        manifest = _read_manifest(folder)
        fm, body = split_frontmatter(entry.read_text(encoding="utf-8"))
        description = (fm.get("description") or manifest.get("description") or "").strip()
        resource_id = manifest.get("id") or folder.name

        resources[resource_id] = Resource(
            id=resource_id,
            name=fm.get("name") or manifest.get("name") or folder.name,
            description=description,
            tags=manifest.get("tags") or fm.get("tags") or [],
            version=str(manifest.get("version") or fm.get("version") or "0.0.0"),
            body=body.strip(),
            folder=folder,
            resource_type=resource_type,
            source=source,
            files=_collect_supporting_files(folder, entry),
        )
    return resources


def merge_resources(*layers: dict[str, Resource]) -> dict[str, Resource]:
    merged: dict[str, Resource] = {}
    for layer in layers:
        for rid, resource in layer.items():
            if rid not in merged:
                merged[rid] = resource
    return merged


def read_lockfile_bundles(catalog_root: Path) -> list[str]:
    """Return bundle ids from agenthub-lock.json if present."""
    lock_path = catalog_root / "agenthub-lock.json"
    if not lock_path.is_file():
        return []
    try:
        import json

        data = json.loads(lock_path.read_text(encoding="utf-8"))
        bundles = data.get("bundles") or []
        return [b for b in bundles if isinstance(b, str) and b.strip()]
    except (OSError, ValueError):
        return []


def discover_catalog_root(explicit: Path | None = None) -> Path:
    if explicit is not None:
        root = explicit.expanduser().resolve()
    else:
        env = os.environ.get("AGENTHUB_CATALOG_PATH")
        if not env:
            raise FileNotFoundError(
                "Agent Hub catalog not found. Set AGENTHUB_CATALOG_PATH, pass catalog_path, "
                "or install with `agenthub install --source https://github.com/BeeNeural-com/agenthub "
                "--target ~/.agenthub`."
            )
        root = Path(env).expanduser().resolve()

    if not (root / "global" / "skills").is_dir():
        raise FileNotFoundError(
            f"Agent Hub catalog at {root} is missing global/skills/. "
            "Install resources with `agenthub install` or point to a valid catalog directory."
        )
    return root


def load_catalog(
    catalog_root: Path,
    bundles: list[str] | None = None,
) -> dict[str, dict[str, Resource]]:
    bundle_names = bundles or []
    if not bundle_names:
        raw = os.environ.get("AGENTHUB_BUNDLE", "")
        bundle_names = [b.strip() for b in raw.split(",") if b.strip()]
    if not bundle_names:
        bundle_names = read_lockfile_bundles(catalog_root)

    result: dict[str, dict[str, Resource]] = {}
    for rtype in RESOURCE_TYPES:
        subdir = SUBDIRS[rtype]
        global_root = catalog_root / "global" / subdir
        layers = [load_resources_from_root(global_root, rtype, "global")]
        for bundle in bundle_names:
            bundle_root = catalog_root / "bundles" / bundle / subdir
            layers.append(load_resources_from_root(bundle_root, rtype, f"bundle:{bundle}"))
        result[rtype] = merge_resources(*layers)
    return result


def read_resource_file(resource: Resource, path: str) -> str | None:
    normalized = path.replace("\\", "/")
    matched = next((f for f in resource.files if f.replace("\\", "/") == normalized), None)
    if matched is None:
        return None
    folder = resource.folder.resolve()
    target = (folder / matched).resolve()
    if not target.is_relative_to(folder) or not target.is_file():
        return None
    return target.read_text(encoding="utf-8")


def load_bundles(catalog_root: Path) -> list[BundleInfo]:
    bundles_dir = catalog_root / "bundles"
    if not bundles_dir.is_dir():
        return []
    out: list[BundleInfo] = []
    for folder in sorted(p for p in bundles_dir.iterdir() if p.is_dir()):
        manifest = _read_manifest(folder)
        out.append(
            BundleInfo(
                id=manifest.get("id") or folder.name,
                name=manifest.get("name") or folder.name,
                description=(manifest.get("description") or "").strip(),
                skill_count=len(list((folder / "skills").iterdir()))
                if (folder / "skills").is_dir()
                else 0,
                agent_count=len(list((folder / "agents").iterdir()))
                if (folder / "agents").is_dir()
                else 0,
                rule_count=len(list((folder / "rules").iterdir()))
                if (folder / "rules").is_dir()
                else 0,
                prompt_count=len(list((folder / "prompts").iterdir()))
                if (folder / "prompts").is_dir()
                else 0,
            )
        )
    return out
