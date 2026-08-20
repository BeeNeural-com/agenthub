from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "sample-catalog"


class McpStartupTests(unittest.TestCase):
    def test_server_module_loads_without_key(self) -> None:
        env = {
            "AGENTHUB_CATALOG_PATH": str(FIXTURES),
        }
        env.pop("AGENTHUB_ACCESS_KEY", None)
        env.pop("AGENTHUB_ACCESS_KEY_SHA256", None)
        with patch.dict(os.environ, env, clear=True):
            import importlib

            import agenthub_mcp.server as server

            importlib.reload(server)
            self.assertEqual(len(server.SKILLS), 1)
            self.assertIn("test-skill", server.SKILLS)

    def test_cli_imports_without_key(self) -> None:
        env = os.environ.copy()
        env.pop("AGENTHUB_ACCESS_KEY", None)
        env.pop("AGENTHUB_ACCESS_KEY_SHA256", None)
        env["AGENTHUB_CATALOG_PATH"] = str(FIXTURES)

        result = subprocess.run(
            [sys.executable, "-c", "import agenthub_mcp.server; print('ok')"],
            capture_output=True,
            text=True,
            env=env,
            timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ok", result.stdout)


if __name__ == "__main__":
    unittest.main()
