"""Install Agent Hub resources locally — full catalog, bundle, or single skill."""
from __future__ import annotations

import json
import shutil
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from agenthub._loader import SUBDIRS, discover_catalog_root
from agenthub._remote import resolve_install_source


@dataclass
class InstallResult:
    target: Path
    installed: list[str] = field(default_factory=list)
    catalog_version: str = "0.1.0"
    source: str = ""


def _copy_tree(src: Path, dst: Path) -> list[str]:
    copied: list[str] = []
    if not src.is_dir():
        return copied
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            copied.extend(_copy_tree(item, target))
        else:
            shutil.copy2(item, target)
            copied.append(str(target.relative_to(dst.parent.parent)))
    return copied


def _write_lockfile(
    target: Path,
    *,
    bundles: list[str],
    resources: list[str],
    source: str = "",
) -> None:
    lock = {
        "lockfileVersion": 1,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "bundles": bundles,
        "resources": resources,
        "catalogPath": str(target),
        "source": source,
    }
    (target / "agenthub-lock.json").write_text(json.dumps(lock, indent=2), encoding="utf-8")


def install(
    target: str | Path,
    *,
    source_catalog: str | Path | None = None,
    bundle: str | None = None,
    skill: str | None = None,
    agent: str | None = None,
    rule: str | None = None,
    prompt: str | None = None,
    full: bool = False,
) -> InstallResult:
    """Install resources into target directory (default .agenthub/).

    Modes (pick one):
      full=True          — entire catalog (global + all bundles)
      bundle="r-and-d"   — one bundle + global
      skill/agent/rule/prompt — single resource folder

    *source_catalog* may be a local path, a GitHub URL, or ``github:owner/repo[@ref]``.
    Remote sources download only ``global/`` + ``bundles/`` (no full repo clone).
    """
    resolved = resolve_install_source(source_catalog)
    src_root = discover_catalog_root(resolved)
    source_label = str(source_catalog) if source_catalog else str(src_root)
    dest = Path(target).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)

    installed: list[str] = []
    bundles_used: list[str] = []

    if full:
        for part in ("global", "bundles"):
            s, d = src_root / part, dest / part
            if s.is_dir():
                installed.extend(_copy_tree(s, d))
        bundles_used = [p.name for p in (src_root / "bundles").iterdir() if p.is_dir()]
    elif bundle:
        bundles_used = [bundle]
        g_src, g_dst = src_root / "global", dest / "global"
        if g_src.is_dir():
            installed.extend(_copy_tree(g_src, g_dst))
        b_src, b_dst = src_root / "bundles" / bundle, dest / "bundles" / bundle
        if b_src.is_dir():
            installed.extend(_copy_tree(b_src, b_dst))
        else:
            raise FileNotFoundError(f"Bundle not found: {bundle}")
    else:
        mapping = {
            "skill": skill,
            "agent": agent,
            "rule": rule,
            "prompt": prompt,
        }
        selected = {k: v for k, v in mapping.items() if v}
        if len(selected) != 1:
            raise ValueError("Specify exactly one of: full, bundle, skill, agent, rule, prompt")

        rtype, rid = next(iter(selected.items()))
        subdir = SUBDIRS[rtype]
        found: Path | None = None

        for root, label in [(src_root / "global", "global"), *[
            (src_root / "bundles" / b, f"bundle:{b}")
            for b in (src_root / "bundles").iterdir()
            if (src_root / "bundles").is_dir() and b.is_dir()
        ]]:
            candidate = root / subdir / rid
            if candidate.is_dir():
                found = candidate
                dest_root = dest / ("global" if label == "global" else f"bundles/{root.name}")
                installed.extend(_copy_tree(candidate, dest_root / subdir / rid))
                if label.startswith("bundle:"):
                    bundles_used.append(root.name)
                break

        if found is None:
            raise FileNotFoundError(f"{rtype} not found: {rid}")

    _write_lockfile(
        dest,
        bundles=list(dict.fromkeys(bundles_used)),
        resources=installed,
        source=source_label,
    )
    return InstallResult(target=dest, installed=installed, source=source_label)
