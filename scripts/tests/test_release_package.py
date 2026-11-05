from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BUILDER = REPO_ROOT / "scripts" / "build_skill_package.py"
SKILL_ROOT = REPO_ROOT / ".agents" / "skills" / "liquid-glass"


class SkillReleasePackageTests(unittest.TestCase):
    def build(self, output: Path) -> None:
        subprocess.run(
            [sys.executable, str(BUILDER), "--output", str(output)],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_package_builder_check(self) -> None:
        result = subprocess.run(
            [sys.executable, str(BUILDER), "--check"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("Validated", result.stdout)

    def test_archive_is_versioned_self_contained_and_excludes_private_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive_path = Path(temporary) / "liquid-glass.zip"
            self.build(archive_path)
            with zipfile.ZipFile(archive_path) as archive:
                names = archive.namelist()
                self.assertIn("liquid-glass/SKILL.md", names)
                self.assertIn("liquid-glass/VERSION", names)
                self.assertIn("liquid-glass/manifest.json", names)
                self.assertIn("liquid-glass/LICENSE", names)
                self.assertIn("liquid-glass/PROVENANCE.md", names)
                self.assertIn("liquid-glass/references/project-docs/platform-adaptation/README.md", names)
                self.assertTrue(all(name.startswith("liquid-glass/") for name in names))
                self.assertFalse(any(name.endswith(".app.json") for name in names))
                self.assertFalse(any(name.lower().endswith((".png", ".jpg", ".jpeg", ".mp4", ".apk")) for name in names))

                version = archive.read("liquid-glass/VERSION").decode("utf-8").strip()
                manifest = json.loads(archive.read("liquid-glass/manifest.json"))
                self.assertEqual(manifest["version"], version)
                self.assertEqual(manifest["entrypoint"], "SKILL.md")
                self.assertFalse(manifest["package_policy"]["private_plugin_binding_included"])
                self.assertFalse(manifest["package_policy"]["user_supplied_visual_references_included"])

                skill = archive.read("liquid-glass/SKILL.md").decode("utf-8")
                self.assertIn("references/project-docs/platform-adaptation/README.md", skill)

                listed_hashes = manifest["sha256"]
                for path, expected in listed_hashes.items():
                    actual = hashlib.sha256(archive.read("liquid-glass/" + path)).hexdigest()
                    self.assertEqual(actual, expected, path)
                self.assertEqual(set(listed_hashes) | {"manifest.json"}, {
                    name.removeprefix("liquid-glass/") for name in names
                })

    def test_zip_build_is_reproducible(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first.zip"
            second = Path(temporary) / "second.zip"
            self.build(first)
            self.build(second)
            self.assertEqual(
                hashlib.sha256(first.read_bytes()).hexdigest(),
                hashlib.sha256(second.read_bytes()).hexdigest(),
            )

    def test_studio_and_skill_versions_are_aligned(self) -> None:
        skill_version = (SKILL_ROOT / "VERSION").read_text(encoding="utf-8").strip()
        plugin = json.loads(
            (REPO_ROOT / "studio" / "package-source" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(plugin["version"], skill_version)


if __name__ == "__main__":
    unittest.main()
