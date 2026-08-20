"""Public Catalog API for agents and applications."""
from __future__ import annotations

import re
from dataclasses import replace
from pathlib import Path

from agenthub._cache import ResourceCache
from agenthub._loader import (
    BundleInfo,
    RagDocument,
    Resource,
    ResourceMeta,
    discover_catalog_root,
    load_bundles,
    load_catalog,
    read_resource_file,
)


class Catalog:
    """Load, search, and export Agent Hub resources."""

    def __init__(
        self,
        catalog_path: str | Path | None = None,
        bundles: list[str] | None = None,
    ) -> None:
        self.root = discover_catalog_root(Path(catalog_path).expanduser() if catalog_path else None)
        self.bundles = bundles
        self._data = load_catalog(self.root, bundles)
        self._cache = ResourceCache(self.root)

    def list_bundles(self) -> list[BundleInfo]:
        return load_bundles(self.root)

    def _pool(self, resource_type: str | None = None) -> list[Resource]:
        if resource_type:
            return list(self._data.get(resource_type, {}).values())
        out: list[Resource] = []
        for pool in self._data.values():
            out.extend(pool.values())
        return out

    def list_skills(self) -> list[ResourceMeta]:
        return [ResourceMeta.from_resource(r) for r in self._data.get("skill", {}).values()]

    def list_agents(self) -> list[ResourceMeta]:
        return [ResourceMeta.from_resource(r) for r in self._data.get("agent", {}).values()]

    def list_rules(self) -> list[ResourceMeta]:
        return [ResourceMeta.from_resource(r) for r in self._data.get("rule", {}).values()]

    def list_prompts(self) -> list[ResourceMeta]:
        return [ResourceMeta.from_resource(r) for r in self._data.get("prompt", {}).values()]

    def get(self, resource_id: str, resource_type: str | None = None) -> Resource | None:
        types = [resource_type] if resource_type else list(self._data.keys())
        for rtype in types:
            if resource_id in self._data.get(rtype, {}):
                resource = self._data[rtype][resource_id]
                body = self._cache.get_or_fetch_body(resource)
                return resource if body == resource.body else replace(resource, body=body)
        return None

    def get_skill(self, skill_id: str) -> Resource | None:
        return self.get(skill_id, "skill")

    def get_agent(self, agent_id: str) -> Resource | None:
        return self.get(agent_id, "agent")

    def get_rule(self, rule_id: str) -> Resource | None:
        return self.get(rule_id, "rule")

    def get_prompt(self, prompt_id: str) -> Resource | None:
        return self.get(prompt_id, "prompt")

    def read_file(self, resource_id: str, path: str, resource_type: str | None = None) -> str | None:
        resource = self.get(resource_id, resource_type)
        if resource is None:
            return None
        return self._cache.get_or_fetch_file(resource, path)

    def search(
        self,
        query: str,
        *,
        resource_type: str | None = None,
        tags: list[str] | None = None,
        limit: int = 10,
    ) -> list[ResourceMeta]:
        q = query.lower()
        tokens = [t for t in re.split(r"\W+", q) if t]
        scored: list[tuple[int, Resource]] = []

        for resource in self._pool(resource_type):
            if tags and not any(t in resource.tags for t in tags):
                continue
            haystack = f"{resource.id} {resource.name} {resource.description} {' '.join(resource.tags)}".lower()
            score = sum(1 for t in tokens if t in haystack)
            if score or not tokens:
                if not tokens or score > 0:
                    scored.append((score, resource))

        scored.sort(key=lambda x: (-x[0], x[1].id))
        return [ResourceMeta.from_resource(r) for _, r in scored[:limit]]

    def as_rag_documents(
        self,
        *,
        resource_types: tuple[str, ...] = ("skill", "agent", "rule", "prompt"),
        include_supporting: bool = False,
    ) -> list[RagDocument]:
        docs: list[RagDocument] = []
        for rtype in resource_types:
            for resource in self._data.get(rtype, {}).values():
                text = f"# {resource.name}\n\n{resource.description}\n\n{resource.body}"
                docs.append(
                    RagDocument(
                        id=f"{rtype}:{resource.id}",
                        text=text,
                        metadata={
                            "id": resource.id,
                            "type": rtype,
                            "name": resource.name,
                            "tags": resource.tags,
                            "version": resource.version,
                            "source": resource.source,
                        },
                    )
                )
                if include_supporting:
                    for rel in resource.files:
                        content = read_resource_file(resource, rel)
                        if content:
                            docs.append(
                                RagDocument(
                                    id=f"{rtype}:{resource.id}:{rel}",
                                    text=content,
                                    metadata={
                                        "id": resource.id,
                                        "type": rtype,
                                        "file": rel,
                                        "parent": resource.id,
                                    },
                                )
                            )
        return docs
