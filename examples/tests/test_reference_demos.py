from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "examples" / "webgl2"
ANDROID = ROOT / "examples" / "android-gles"


class ReferenceDemoTests(unittest.TestCase):
    def test_web_demo_has_an_owned_texture_refraction_pipeline(self) -> None:
        html = (WEB / "index.html").read_text(encoding="utf-8")
        source = (WEB / "src" / "main.js").read_text(encoding="utf-8")
        css = (WEB / "styles.css").read_text(encoding="utf-8")
        manifest = json.loads((WEB / "package.json").read_text(encoding="utf-8"))

        self.assertIn('getContext("webgl2"', source)
        self.assertIn("createFramebuffer()", source)
        self.assertIn("framebufferTexture2D", source)
        self.assertIn("texture(uScene", source)
        self.assertIn("lensDistance", source)
        self.assertIn("smoothUnion", source)
        self.assertIn("uMorph", source)
        self.assertIn('id="scene"', html)
        self.assertIn('id="morph-toggle"', html)
        self.assertIn('id="progress"', html)
        self.assertIn("prefers-reduced-motion", css)
        self.assertIn("playwright", manifest["devDependencies"])

    def test_web_demo_labels_fallback_separately_from_l2(self) -> None:
        readme = (WEB / "README.md").read_text(encoding="utf-8").lower()
        source = (WEB / "src" / "main.js").read_text(encoding="utf-8")
        self.assertIn("l2", readme)
        self.assertIn("l3", readme)
        self.assertIn("l1", readme)
        self.assertIn("css-l1", source)
        self.assertIn("css-l0", source)
        self.assertIn("not css backdrop blur", readme)

    def test_android_project_declares_compatibility_and_compiles_native_semantics(self) -> None:
        gradle = (ANDROID / "app" / "build.gradle").read_text(encoding="utf-8")
        manifest_path = ANDROID / "app" / "src" / "main" / "AndroidManifest.xml"
        manifest = ET.parse(manifest_path).getroot()
        activity = (ANDROID / "app" / "src" / "main" / "java" /
                    "org" / "liquidglass" / "reference" / "MainActivity.java").read_text(encoding="utf-8")
        renderer = (ANDROID / "app" / "src" / "main" / "java" /
                    "org" / "liquidglass" / "reference" / "GlassRenderer.java").read_text(encoding="utf-8")

        self.assertIn("compileSdk 35", gradle)
        self.assertIn("minSdk 23", gradle)
        self.assertIn("targetSdk 35", gradle)
        uses_feature = manifest.find("uses-feature")
        self.assertIsNotNone(uses_feature)
        self.assertEqual(uses_feature.attrib.get("{http://schemas.android.com/apk/res/android}glEsVersion"), "0x00020000")
        self.assertIn("new Button", activity)
        self.assertIn("new SeekBar", activity)
        self.assertIn("setContentDescription", activity)
        self.assertIn("glFramebufferTexture2D", renderer)
        self.assertIn("texture2D(uScene", renderer)
        self.assertIn("GL_READY tier=L3", renderer)
        self.assertIn("GL_FALLBACK tier=L0", renderer)
        self.assertIn("smoothstep", renderer)

    def test_android_demo_documents_actual_fidelity_and_boundaries(self) -> None:
        readme = (ANDROID / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("l2", readme)
        self.assertIn("l3", readme)
        self.assertIn("l0", readme)
        self.assertIn("does not sample arbitrary android view hierarchies", readme)
        self.assertIn("emulator", readme)

    def test_both_demos_have_reproducible_visual_capture_routes(self) -> None:
        web_test = (WEB / "tests" / "smoke.mjs").read_text(encoding="utf-8")
        workflow = (ROOT / ".github" / "workflows" / "reference-demos.yml").read_text(encoding="utf-8")
        self.assertIn("webgl2-desktop.png", web_test)
        self.assertIn("webgl2-mobile.png", web_test)
        self.assertIn("GL_READY tier=L3", workflow)
        self.assertIn("adb shell screencap", workflow)
        self.assertIn("upload-artifact@v4", workflow)


if __name__ == "__main__":
    unittest.main()
