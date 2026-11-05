from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

STUDIO_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = STUDIO_ROOT.parent
BUILDER = STUDIO_ROOT / "scripts" / "build_plugin_package.py"


class StudioPackageTests(unittest.TestCase):
    def test_package_builder_compiles_and_validates(self) -> None:
        result = subprocess.run(
            [sys.executable, str(BUILDER), "--check"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("Validated", result.stdout)

    def test_private_plugin_archive_inventory_and_binding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive_path = Path(temporary) / "studio.zip"
            subprocess.run(
                [sys.executable, str(BUILDER), "--output", str(archive_path)],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            with zipfile.ZipFile(archive_path) as archive:
                names = archive.namelist()
                self.assertIn("plugin.json", names)
                self.assertIn(".app.json", names)
                self.assertIn("LICENSE", names)
                self.assertIn("PROVENANCE.md", names)
                self.assertIn("skills/liquid-glass-studio/SKILL.md", names)
                self.assertTrue(all(not name.startswith(("liquid-glass-studio/", "studio/")) for name in names))
                manifest = json.loads(archive.read("plugin.json"))
                app = json.loads(archive.read(".app.json"))
                self.assertEqual(manifest["name"], "liquid-glass-studio")
                skill_version = (REPO_ROOT / ".agents" / "skills" / "liquid-glass" / "VERSION").read_text(encoding="utf-8").strip()
                self.assertEqual(manifest["version"], skill_version)
                self.assertEqual(manifest["extensions"]["com.openai"]["apps"], "./.app.json")
                self.assertEqual(app["apps"]["github"]["id"], "connector_76869538009648d5b282a4bb21c3d157")

    def test_short_description_and_workflow_contracts(self) -> None:
        manifest = json.loads((STUDIO_ROOT / "package-source" / "plugin.json").read_text(encoding="utf-8"))
        interface = manifest["extensions"]["com.openai"]["interface"]
        self.assertLessEqual(len(interface["shortDescription"]), 30)
        self.assertEqual(interface["category"], "Developer Tools")
        skill = (STUDIO_ROOT / "package-source" / "skills" / "liquid-glass-studio" / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = skill.split("---\n", 2)[1]
        self.assertIn("name: liquid-glass-studio", frontmatter)
        for operation in (
            "analyze_reference", "create_visual_brief", "diagnose_project",
            "select_strategy", "implement_glass", "review_implementation",
            "audit_performance_accessibility",
        ):
            self.assertIn(operation, skill)

    def test_manifest_does_not_fabricate_an_mcp_endpoint(self) -> None:
        self.assertFalse((STUDIO_ROOT / "package-source" / "mcp.json").exists())
        app = json.loads((STUDIO_ROOT / "package-source" / ".app.json").read_text(encoding="utf-8"))
        self.assertEqual(app["apps"]["github"]["id"], "connector_76869538009648d5b282a4bb21c3d157")


if __name__ == "__main__":
    unittest.main()
