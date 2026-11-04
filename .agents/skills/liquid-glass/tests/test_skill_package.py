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
REPO_ROOT = SKILL_DIR.parents[2]
INSPECTOR = SKILL_DIR / "scripts" / "inspect_project.py"
EXAMPLES = SKILL_DIR / "examples"
PLATFORM_DOCS = REPO_ROOT / "docs" / "platform-adaptation"

PLATFORM_GUIDES = (
    "README.md",
    "capability-matrix.md",
    "web.md",
    "android.md",
    "android-library-catalog.md",
    "apple.md",
    "desktop.md",
    "game-engines.md",
    "cross-platform.md",
    "constrained.md",
)

PLATFORM_WORKFLOWS = (
    "apple-swiftui/WORKFLOW.md",
    "windows-winui/WORKFLOW.md",
    "qt6-quick/WORKFLOW.md",
    "flutter/WORKFLOW.md",
    "unity-urp/WORKFLOW.md",
    "unreal-postprocess/WORKFLOW.md",
    "constrained-fallback/WORKFLOW.md",
)


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
        for policy in ("existing app", "new app", "minSdk", "Build.VERSION.SDK_INT", "33+"):
            self.assertIn(policy.lower(), trace)

    def test_platform_neutrality_and_tier_honesty(self) -> None:
        content = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("do not force one language", content)
        self.assertIn("blur is not refraction", content)
        for tier in ("l0", "l1", "l2", "l3"):
            self.assertIn(tier, content)

    def test_platform_adaptation_guides_and_workflows_cover_candidate_families(self) -> None:
        for relative_path in PLATFORM_GUIDES:
            guide = PLATFORM_DOCS / relative_path
            self.assertTrue(guide.is_file(), f"Missing platform guide: {relative_path}")

        android = (PLATFORM_DOCS / "android.md").read_text(encoding="utf-8").lower()
        catalog = (PLATFORM_DOCS / "android-library-catalog.md").read_text(encoding="utf-8").lower()
        for policy in ("existing project", "new project", "minsdk", "build.version.sdk_int", "runtime", "opengl es"):
            self.assertIn(policy, android)
        for candidate in ("blurview", "haze", "miuix-blur", "rive", "realtimeblurview", "version-4.0.0", "2.1.0", "api 33+"):
            self.assertIn(candidate, catalog)
        self.assertIn("refraction", catalog)
        matrix = (PLATFORM_DOCS / "capability-matrix.md").read_text(encoding="utf-8").lower()
        for column in ("backdrop access", "refraction route", "shader", "masks and motion", "accessibility integration", "version / hardware gate"):
            self.assertIn(column, matrix)
        for source_domain in (
            "developer.mozilla.org",
            "developer.android.com",
            "developer.apple.com",
            "learn.microsoft.com",
            "doc.qt.io",
            "api.flutter.dev",
            "docs.unity.com",
            "dev.epicgames.com",
        ):
            self.assertIn(source_domain, matrix)

        self.assertTrue((EXAMPLES / "README.md").is_file(), "Missing platform workflow catalog")
        required_workflows = ("web-dom/WORKFLOW.md", "android-java/WORKFLOW.md") + PLATFORM_WORKFLOWS
        for relative_path in required_workflows:
            workflow = EXAMPLES / relative_path
            self.assertTrue(workflow.is_file(), f"Missing platform workflow: {relative_path}")
            content = workflow.read_text(encoding="utf-8").lower()
            self.assertIn("validation", content, f"No validation instructions in {relative_path}")
            self.assertTrue(any(tier in content for tier in ("l0", "l1", "l2", "l3")), f"No fidelity tier in {relative_path}")

    def test_platform_documentation_links_resolve(self) -> None:
        markdown_files = list(PLATFORM_DOCS.rglob("*.md")) + list(EXAMPLES.rglob("*.md"))
        markdown_files += [
            SKILL_DIR / "SKILL.md",
            SKILL_DIR / "README.md",
            SKILL_DIR / "INSTALL.md",
            REPO_ROOT / "README.md",
            REPO_ROOT / "GPT.md",
            REPO_ROOT / "docs" / "README.md",
            REPO_ROOT / "docs" / "skill-installation.md",
        ]
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        failures = []
        for markdown_file in markdown_files:
            source = markdown_file.read_text(encoding="utf-8")
            for destination in link_pattern.findall(source):
                destination = destination.strip()
                if not destination or destination.startswith(("#", "https://", "http://", "mailto:")):
                    continue
                destination = destination.split("#", 1)[0].split("?", 1)[0]
                if not destination:
                    continue
                target = (markdown_file.parent / destination).resolve()
                if not target.exists():
                    failures.append(f"{markdown_file.relative_to(REPO_ROOT)} -> {destination}")
        self.assertEqual(failures, [], "Broken local Markdown links:\n" + "\n".join(failures))

    def test_chatgpt_desktop_personal_install_path_is_correct(self) -> None:
        install = (SKILL_DIR / "INSTALL.md").read_text(encoding="utf-8")
        root_guide = (REPO_ROOT / "docs" / "skill-installation.md").read_text(encoding="utf-8")
        self.assertIn('$HOME\\.codex\\skills', install)
        self.assertIn('%USERPROFILE%\\.codex\\skills\\liquid-glass\\SKILL.md', install)
        self.assertIn('$HOME\\.codex\\skills', root_guide)
        self.assertNotIn('~/.agents/skills', install + root_guide)
        self.assertNotIn('$skill-installer', install + root_guide)
        self.assertIn('backed up', install.lower())


if __name__ == "__main__":
    unittest.main()
