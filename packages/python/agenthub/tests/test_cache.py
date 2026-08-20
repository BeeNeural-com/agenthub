from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agenthub._cache import LOCKFILE_NAME, ResourceCache, discover_cache_path
from agenthub._loader import Resource

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "sample-catalog"


def _sample_resource(version: str = "1.0.0") -> Resource:
    return Resource(
        id="test-skill",
        name="Test Skill",
        description="Fixture skill",
        tags=["demo"],
        version=version,
        body="Fixture body for cache tests.",
        folder=FIXTURES / "global" / "skills" / "test-skill",
        resource_type="skill",
        source="global",
        files=["references/template.md"],
    )


class CacheTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory()
        self.cache_dir = Path(self._tmpdir.name) / ".agenthub-cache"
        self.env = {"AGENTHUB_CACHE_PATH": str(self.cache_dir)}

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_discover_cache_path_prefers_env(self) -> None:
        with patch.dict(os.environ, {"AGENTHUB_CACHE_PATH": str(self.cache_dir)}, clear=False):
            resolved = discover_cache_path(FIXTURES)
            self.assertEqual(resolved, self.cache_dir.resolve())

    def test_cache_miss_then_hit(self) -> None:
        resource = _sample_resource()
        with patch.dict(os.environ, self.env, clear=False):
            cache = ResourceCache(FIXTURES, cache_path=self.cache_dir)
            self.assertIsNone(cache.get_body("skill", "test-skill", resource.version))

            body = cache.get_or_fetch_body(resource)
            self.assertEqual(body, resource.body)

            cached = cache.get_body("skill", "test-skill", resource.version)
            self.assertEqual(cached, resource.body)

            lock_path = self.cache_dir / LOCKFILE_NAME
            self.assertTrue(lock_path.is_file())
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
            self.assertEqual(lock["lockfileVersion"], 1)
            self.assertEqual(len(lock["entries"]), 1)
            self.assertEqual(lock["entries"][0]["id"], "test-skill")

    def test_version_invalidation(self) -> None:
        resource_v1 = _sample_resource("1.0.0")
        resource_v2 = _sample_resource("2.0.0")
        resource_v2.body = "Updated body."

        with patch.dict(os.environ, self.env, clear=False):
            cache = ResourceCache(FIXTURES, cache_path=self.cache_dir)
            cache.get_or_fetch_body(resource_v1)
            self.assertEqual(cache.get_body("skill", "test-skill", "1.0.0"), resource_v1.body)
            self.assertIsNone(cache.get_body("skill", "test-skill", "2.0.0"))

            body = cache.get_or_fetch_body(resource_v2)
            self.assertEqual(body, "Updated body.")
            self.assertEqual(cache.get_body("skill", "test-skill", "2.0.0"), "Updated body.")

    def test_clear_removes_entries(self) -> None:
        resource = _sample_resource()
        with patch.dict(os.environ, self.env, clear=False):
            cache = ResourceCache(FIXTURES, cache_path=self.cache_dir)
            cache.get_or_fetch_body(resource)
            self.assertEqual(cache.status()["entryCount"], 1)

            cache.clear()
            status = cache.status()
            self.assertEqual(status["entryCount"], 0)
            self.assertIsNone(cache.get_body("skill", "test-skill", resource.version))

    def test_cache_works_without_access_key(self) -> None:
        env = {k: v for k, v in os.environ.items() if k not in ("AGENTHUB_ACCESS_KEY", "AGENTHUB_ACCESS_KEY_SHA256")}
        with patch.dict(os.environ, {**env, "AGENTHUB_CACHE_PATH": str(self.cache_dir)}, clear=True):
            cache = ResourceCache(FIXTURES, cache_path=self.cache_dir)
            self.assertEqual(cache.status()["entryCount"], 0)


if __name__ == "__main__":
    unittest.main()
