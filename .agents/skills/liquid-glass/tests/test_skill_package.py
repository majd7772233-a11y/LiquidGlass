from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
INSPECTOR = SKILL_DIR / "scripts" / "inspect_project.py"
EXAMPLES = SKILL_DIR / "examples"


class SkillPackageTests(unittest.TestCase):
    def test_required_skill_manifest_and_directory_name(self) -> None:
        content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))
        frontmatter = content.split("---\n", 2)[1]
        name_match = re.search(r"^name:\s*([^\s#]+)\s*$", frontmatter, re.M)
        desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
        self.assertIsNotNone(name_match)
        self.assertIsNotNone(desc_match)
        self.assertEqual(name_match.group(1), SKILL_DIR.name)
        self.assertRegex(name_match.group(1), r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        self.assertLessEqual(len(desc_match.group(1)), 1024)
        self.assertIn("any programming language", desc_match.group(1))

    def test_skill_reference_links_resolve_inside_package(self) -> None:
        content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", content)
        for link in links:
            if "://" in link or link.startswith("#"):
                continue
            target = (SKILL_DIR / link).resolve()
            self.assertTrue(target.exists(), f"Broken skill reference: {link}")
        for required in ("project-discovery.md", "rendering-strategy.md", "visual-contract.md", "motion-accessibility-performance.md", "validation-and-reporting.md"):
            self.assertTrue((SKILL_DIR / "references" / required).is_file())

    def run_inspector(self, fixture: Path) -> dict:
        result = subprocess.run(
            [sys.executable, str(INSPECTOR), str(fixture)],
            check=True, capture_output=True, text=True,
        )
        return json.loads(result.stdout)

    def test_web_dom_end_to_end_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "src").mkdir()
            (project / "package.json").write_text(json.dumps({"devDependencies": {"vite": "^6.0.0"}}), encoding="utf-8")
            (project / "index.html").write_text("<!doctype html><html><body><main id='app'></main></body></html>", encoding="utf-8")
            (project / "src" / "main.ts").write_text('import "./style.css";\n', encoding="utf-8")
            (project / "src" / "style.css").write_text(".glass { backdrop-filter: blur(12px); } /* L1: no backdrop displacement */\n", encoding="utf-8")
            result = self.run_inspector(project)
            families = {item["family"] for item in result["platform_candidates"]}
            self.assertIn("web-dom", families)
            self.assertTrue(any("package.json" in e for c in result["platform_candidates"] for e in c["evidence"]))
            self.assertIn("backdrop-filter", (project / "src" / "style.css").read_text(encoding="utf-8"))
        trace = (EXAMPLES / "web-dom" / "WORKFLOW.md").read_text(encoding="utf-8").lower()
        for stage in ("discovery", "strategy decision", "implementation", "validation", "report"):
            self.assertIn(stage, trace)
        self.assertIn("l1", trace)
        self.assertIn("not l2", trace)

    def test_android_java_xml_end_to_end_workflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "app" / "src" / "main" / "res" / "layout").mkdir(parents=True)
            (project / "app" / "src" / "main" / "java").mkdir(parents=True)
            (project / "settings.gradle").write_text('rootProject.name = "Fixture"\ninclude(":app")\n', encoding="utf-8")
            (project / "app" / "build.gradle").write_text("android { defaultConfig { minSdk 23 } }\n", encoding="utf-8")
            manifest = project / "app" / "src" / "main" / "AndroidManifest.xml"
            manifest.write_text('<manifest xmlns:android="http://schemas.android.com/apk/res/android"><application /></manifest>', encoding="utf-8")
            layout = project / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml"
            layout.write_text('<Button xmlns:android="http://schemas.android.com/apk/res/android" android:id="@+id/glass_action" />', encoding="utf-8")
            (project / "app" / "src" / "main" / "java" / "MainActivity.java").write_text("class MainActivity { /* Java + XML */ }", encoding="utf-8")
            result = self.run_inspector(project)
            families = {item["family"] for item in result["platform_candidates"]}
            self.assertIn("android-native", families)
            self.assertEqual(result["minimum_android_sdk_observed"], 23)
            ET.parse(manifest)
            ET.parse(layout)
        trace = (EXAMPLES / "android-java" / "WORKFLOW.md").read_text(encoding="utf-8").lower()
        for stage in ("discovery", "strategy decision", "implementation", "validation", "report"):
            self.assertIn(stage, trace)
        self.assertIn("l0", trace)
        self.assertIn("does not", trace)

    def test_platform_neutrality_and_tier_honesty(self) -> None:
        content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("do not force one language", content)
        self.assertIn("blur is not refraction", content)
        for tier in ("l0", "l1", "l2", "l3"):
            self.assertIn(tier, content)


if __name__ == "__main__":
    unittest.main()
