from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agenthub._auth import require_access_key
from agenthub.catalog import Catalog
from agenthub.connect import mcp_config_stdio

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "sample-catalog"


class AuthTests(unittest.TestCase):
    def test_require_access_key_is_noop_without_key(self) -> None:
        env = {k: v for k, v in os.environ.items() if k not in ("AGENTHUB_ACCESS_KEY", "AGENTHUB_ACCESS_KEY_SHA256")}
        with patch.dict(os.environ, env, clear=True):
            self.assertEqual(require_access_key(), "")

    def test_require_access_key_returns_key_when_set(self) -> None:
        with patch.dict(os.environ, {"AGENTHUB_ACCESS_KEY": "dev-key"}, clear=False):
            self.assertEqual(require_access_key(), "dev-key")


class CatalogTests(unittest.TestCase):
    def test_loads_fixture_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cache_dir = Path(tmp) / "cache"
            with patch.dict(os.environ, {"AGENTHUB_CACHE_PATH": str(cache_dir)}, clear=False):
                catalog = Catalog(catalog_path=FIXTURES)
                skills = catalog.list_skills()
                self.assertEqual(len(skills), 1)
                self.assertEqual(skills[0].id, "test-skill")
                skill = catalog.get_skill("test-skill")
                self.assertIsNotNone(skill)
                assert skill is not None
                self.assertIn("Fixture body", skill.body)
                self.assertTrue((cache_dir / "agenthub-cache-lock.json").is_file())

    def test_catalog_works_without_access_key(self) -> None:
        env = {k: v for k, v in os.environ.items() if k not in ("AGENTHUB_ACCESS_KEY", "AGENTHUB_ACCESS_KEY_SHA256")}
        with patch.dict(os.environ, env, clear=True):
            catalog = Catalog(catalog_path=FIXTURES)
            self.assertEqual(len(catalog.list_skills()), 1)


class ConnectTests(unittest.TestCase):
    def test_stdio_config_uses_agenthub_mcp_binary(self) -> None:
        cfg = mcp_config_stdio(catalog_path=FIXTURES)
        entry = cfg["mcpServers"]["agenthub"]
        self.assertEqual(entry["command"], "agenthub-mcp")
        self.assertEqual(entry["args"], ["--stdio"])

    def test_stdio_config_omits_access_key(self) -> None:
        with patch.dict(os.environ, {"AGENTHUB_ACCESS_KEY": "my-key"}, clear=False):
            cfg = mcp_config_stdio(catalog_path=FIXTURES)
            env = cfg["mcpServers"]["agenthub"]["env"]
            self.assertNotIn("AGENTHUB_ACCESS_KEY", env)
            self.assertIn("AGENTHUB_CATALOG_PATH", env)

    def test_stdio_config_includes_cache_path_when_set(self) -> None:
        with patch.dict(os.environ, {"AGENTHUB_CACHE_PATH": "D:/cache"}, clear=False):
            cfg = mcp_config_stdio(catalog_path=FIXTURES)
            env = cfg["mcpServers"]["agenthub"]["env"]
            self.assertEqual(env["AGENTHUB_CACHE_PATH"], "D:/cache")


if __name__ == "__main__":
    unittest.main()
