from __future__ import annotations

import io
import zipfile
import unittest
from pathlib import Path
from unittest.mock import patch

from agenthub._remote import (
    DEFAULT_SOURCE,
    GitHubRef,
    fetch_github_catalog,
    parse_github_source,
    resolve_install_source,
)
from agenthub.install import install


def _make_catalog_zip() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        root = "BeeNeural-com-agenthub-abc123"
        zf.writestr(f"{root}/global/skills/demo/SKILL.md", "---\nname: Demo\n---\nBody\n")
        zf.writestr(
            f"{root}/global/skills/demo/manifest.yaml",
            "id: demo\nname: Demo\ndescription: d\nversion: 0.1.0\n",
        )
        zf.writestr(f"{root}/bundles/web-development/manifest.yaml", "id: web-development\nname: Web\n")
        zf.writestr(
            f"{root}/bundles/web-development/skills/web-skill/SKILL.md",
            "---\nname: Web Skill\n---\nWeb\n",
        )
        zf.writestr(
            f"{root}/bundles/web-development/skills/web-skill/manifest.yaml",
            "id: web-skill\nname: Web Skill\nversion: 0.1.0\n",
        )
        # Noise outside catalog — should be skipped
        zf.writestr(f"{root}/packages/python/agenthub/pyproject.toml", "[project]\nname='x'\n")
        zf.writestr(f"{root}/README.md", "# Agent Hub\n")
    return buf.getvalue()


class ParseGitHubSourceTests(unittest.TestCase):
    def test_shorthand(self) -> None:
        ref = parse_github_source("github:BeeNeural-com/agenthub@main")
        self.assertEqual(ref, GitHubRef("BeeNeural-com", "agenthub", "main"))

    def test_https_url(self) -> None:
        ref = parse_github_source("https://github.com/BeeNeural-com/agenthub")
        self.assertEqual(ref.owner, "BeeNeural-com")
        self.assertEqual(ref.repo, "agenthub")
        self.assertEqual(ref.ref, "main")

    def test_https_git_suffix(self) -> None:
        ref = parse_github_source("https://github.com/BeeNeural-com/agenthub.git")
        self.assertIsNotNone(ref)
        assert ref is not None
        self.assertEqual(ref.repo, "agenthub")

    def test_default_source_parses(self) -> None:
        self.assertIsNotNone(parse_github_source(DEFAULT_SOURCE))

    def test_local_path_returns_none(self) -> None:
        self.assertIsNone(parse_github_source(r"C:\local\catalog"))


class FetchGitHubCatalogTests(unittest.TestCase):
    def test_fetch_extracts_only_catalog(self) -> None:
        zip_bytes = _make_catalog_zip()

        class _Resp:
            def read(self) -> bytes:
                return zip_bytes

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        with patch("agenthub._remote.urllib.request.urlopen", return_value=_Resp()):
            import tempfile

            with tempfile.TemporaryDirectory() as tmp:
                dest = fetch_github_catalog(
                    GitHubRef("BeeNeural-com", "agenthub", "main"),
                    cache_dir=Path(tmp),
                    force=True,
                )
                self.assertTrue((dest / "global" / "skills" / "demo").is_dir())
                self.assertTrue((dest / "bundles" / "web-development").is_dir())
                self.assertFalse((dest / "packages").exists())
                self.assertFalse((dest / "README.md").exists())

    def test_install_from_resolved_remote(self) -> None:
        zip_bytes = _make_catalog_zip()

        class _Resp:
            def read(self) -> bytes:
                return zip_bytes

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        with patch("agenthub._remote.urllib.request.urlopen", return_value=_Resp()):
            import tempfile

            with tempfile.TemporaryDirectory() as tmp:
                cache = Path(tmp) / "cache"
                target = Path(tmp) / ".agenthub"
                with patch.dict("os.environ", {"AGENTHUB_CACHE_PATH": str(cache)}, clear=False):
                    result = install(
                        target,
                        source_catalog="https://github.com/BeeNeural-com/agenthub",
                        full=True,
                    )
                self.assertTrue((result.target / "global" / "skills" / "demo").is_dir())
                self.assertGreater(len(result.installed), 0)
                self.assertIn("BeeNeural-com", result.source)


class ResolveInstallSourceTests(unittest.TestCase):
    def test_local_fixture(self) -> None:
        fixtures = Path(__file__).resolve().parent / "fixtures" / "sample-catalog"
        resolved = resolve_install_source(fixtures)
        self.assertEqual(resolved, fixtures.resolve())


if __name__ == "__main__":
    unittest.main()
