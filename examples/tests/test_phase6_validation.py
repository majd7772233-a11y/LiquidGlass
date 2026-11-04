from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "examples" / "webgl2"
ANDROID = ROOT / "examples" / "android-gles"
VALIDATION = ROOT / "examples" / "validation"


class PhaseSixValidationTests(unittest.TestCase):
    def test_visual_review_protocol_and_record_template_are_present(self) -> None:
        guide = (VALIDATION / "README.md").read_text(encoding="utf-8")
        template = (VALIDATION / "visual-review-template.md").read_text(encoding="utf-8")
        for term in ("Visual comparison procedure", "dark backdrop", "bright backdrop",
                     "high-frequency", "Physical-device profiling protocol",
                     "GPU execution time", "TalkBack", "four independent"):
            self.assertIn(term, guide)
        for term in ("Capture matrix", "Visual criteria", "Accessibility review",
                     "Performance record", "Release blockers"):
            self.assertIn(term, template)

    def test_web_renderer_exposes_multi_background_and_runtime_diagnostics(self) -> None:
        source = (WEB / "src" / "main.js").read_text(encoding="utf-8")
        styles = (WEB / "styles.css").read_text(encoding="utf-8")
        smoke = (WEB / "tests" / "smoke.mjs").read_text(encoding="utf-8")
        for token in ("uBackgroundMode", "detailed", "window.__liquidGlassDiagnostics",
                      "averageFrameMs", "p95CpuSubmitMs", "estimatedSceneTextureBytes",
                      "document.hidden", "cancelAnimationFrame"):
            self.assertIn(token, source)
        for token in ("prefers-contrast: more", "prefers-reduced-transparency",
                      "forced-colors: active", "min-height: 44px"):
            self.assertIn(token, styles)
        for token in ("desktop-midnight", "tablet-bright", "mobile-detailed",
                      "landscape-bright", "reducedMotion", "forcedColors",
                      "Keyboard focus", "gpuTimeMs"):
            self.assertIn(token, smoke)

    def test_android_renderer_is_demand_driven_and_measures_frame_pacing(self) -> None:
        activity_path = ANDROID / "app" / "src" / "main" / "java" / "org" / "liquidglass" / "reference" / "MainActivity.java"
        renderer_path = ANDROID / "app" / "src" / "main" / "java" / "org" / "liquidglass" / "reference" / "GlassRenderer.java"
        activity = activity_path.read_text(encoding="utf-8")
        renderer = renderer_path.read_text(encoding="utf-8")
        manifest = (ANDROID / "app" / "src" / "main" / "AndroidManifest.xml").read_text(encoding="utf-8")
        self.assertIn("RENDERMODE_WHEN_DIRTY", activity)
        self.assertIn("framePump", activity)
        self.assertIn("isHighTextContrastEnabled", activity)
        self.assertIn("isReducedMotionEnabled", activity)
        self.assertIn("dp(48)", activity)
        self.assertIn("extra_surfaces", activity)
        self.assertNotIn('android:screenOrientation="portrait"', manifest)
        for token in ("PERF window_frames", "p95_frame_ms", "jank_gt_16_7",
                      "cpu_submit_p95_ms", "fbo_texture_bytes", "full_screen_passes=2", "surfaces=%d", "gpu_time_ms=unavailable",
                      "allSurfaces", "uExtraCount"):
            self.assertIn(token, renderer)

    def test_android_emulator_scripts_capture_accessibility_resizing_multi_surface_and_profile(self) -> None:
        verify = (ANDROID / "scripts" / "verify-emulator.sh").read_text(encoding="utf-8")
        profile = (ANDROID / "scripts" / "profile-emulator.sh").read_text(encoding="utf-8")
        for token in ("android-accessibility-report.json", "minimum_action_target_dp",
                      "wm size 720x1280", "wm size 1280x720",
                      "android-gles2-landscape.png", "extra_surfaces 3",
                      "SURFACE_COUNT main=1 additional=3 total=4"):
            self.assertIn(token, verify)
        for token in ("dumpsys gfxinfo", "dumpsys meminfo", "dumpsys battery",
                      "dumpsys thermalservice", "SurfaceFlinger", "android-performance-summary.json",
                      "--ei extra_surfaces 3"):
            self.assertIn(token, profile)

    def test_ci_runs_and_uploads_phase_six_evidence(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "reference-demos.yml").read_text(encoding="utf-8")
        validation_workflow = (ROOT / ".github" / "workflows" / "skill-validation.yml").read_text(encoding="utf-8")
        self.assertIn("bash -n examples/android-gles/scripts/profile-emulator.sh", workflow)
        self.assertIn("bash examples/android-gles/scripts/profile-emulator.sh", workflow)
        self.assertIn("artifacts/", workflow)
        self.assertIn("upload-artifact@v4", workflow)
        self.assertIn("examples/tests/test_phase6_validation.py", validation_workflow)


if __name__ == "__main__":
    unittest.main()
