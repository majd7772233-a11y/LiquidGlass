#!/usr/bin/env python3
"""Read-only, dependency-free project inventory for the Liquid Glass skill.

This script collects file/configuration evidence. It deliberately does not infer
which renderer should be selected and does not modify the inspected project.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

SKIP_DIRS = {
    ".git", ".hg", ".svn", ".idea", ".gradle", ".venv", "venv",
    "node_modules", "vendor", "build", "dist", "out", "target",
    "Pods", "DerivedData", ".next", ".turbo", "coverage", "__pycache__", ".pytest_cache",
}
MAX_FILES = 12000
MAX_READ_BYTES = 1_000_000


def walk_files(root: Path) -> list[str]:
    found: list[str] = []
    for current, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(names):
            path = Path(current) / name
            try:
                rel = path.relative_to(root).as_posix()
            except ValueError:
                continue
            found.append(rel)
            if len(found) >= MAX_FILES:
                return found
    return found


def read_text(path: Path) -> str:
    try:
        with path.open("rb") as handle:
            data = handle.read(MAX_READ_BYTES)
        return data.decode("utf-8", errors="replace")
    except (OSError, UnicodeError):
        return ""


def inspect(root_arg: str) -> dict[str, Any]:
    root = Path(root_arg).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Project root is not a directory: {root}")

    paths = walk_files(root)
    lower = {p.lower() for p in paths}
    candidates: list[dict[str, Any]] = []
    languages: set[str] = set()
    build_tools: set[str] = set()
    graphics: set[str] = set()
    evidence: dict[str, list[str]] = {}

    def add_signal(family: str, item: str) -> None:
        evidence.setdefault(family, []).append(item)

    # Browser/web evidence.
    web_paths = [p for p in paths if p.lower().endswith((".html", ".css", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte"))]
    if web_paths:
        languages.add("JavaScript/TypeScript/HTML/CSS (source extensions observed)")
    for marker in ("package.json", "vite.config.ts", "vite.config.js", "next.config.js", "next.config.mjs", "next.config.ts", "astro.config.mjs", "angular.json"):
        if marker in lower:
            add_signal("web-dom", marker)
    if any(p.lower().endswith(".html") for p in paths):
        add_signal("web-dom", "HTML document")
    if any(p.lower().endswith((".css", ".scss", ".sass")) for p in paths):
        add_signal("web-dom", "stylesheet source")
    pkg = root / "package.json"
    if pkg.is_file():
        try:
            data = json.loads(read_text(pkg))
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            for dep in ("react", "vue", "svelte", "next", "vite", "angular", "three", "playwright"):
                if dep in deps:
                    add_signal("web-dom", f"package dependency: {dep}")
            if deps:
                build_tools.add("npm-compatible package manifest")
        except (json.JSONDecodeError, TypeError):
            add_signal("web-dom", "package.json present but unreadable as valid JSON")

    # Android evidence.
    android_manifest = any(p.lower().endswith("androidmanifest.xml") for p in paths)
    gradle_paths = [p for p in paths if Path(p).name.lower() in {"build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts"}]
    java_paths = [p for p in paths if p.lower().endswith(".java")]
    kotlin_paths = [p for p in paths if p.lower().endswith(".kt")]
    if android_manifest:
        add_signal("android-native", "AndroidManifest.xml")
    if gradle_paths:
        add_signal("android-native", "Gradle build/settings file")
        build_tools.add("Gradle")
    if java_paths:
        languages.add("Java")
    if kotlin_paths:
        languages.add("Kotlin")
    for p in paths:
        if p.lower().endswith(".xml") and ("/res/" in p.lower() or "/src/main/" in p.lower()):
            add_signal("android-native", "Android XML resource/source")
            break
    min_sdk = None
    gradle_text = "\n".join(read_text(root / p) for p in gradle_paths)
    match = re.search(r"\bminSdk(?:Version)?\s*(?:=\s*)?(?:\(?\s*)?(\d+)", gradle_text, re.IGNORECASE)
    if match:
        min_sdk = int(match.group(1))
        add_signal("android-native", f"minSdk evidence: {min_sdk}")

    # Apple/native evidence.
    apple_paths = [p for p in paths if p.lower().endswith((".swift", ".m", ".mm")) or ".xcodeproj/" in p.lower() or ".xcworkspace/" in p.lower()]
    if apple_paths:
        add_signal("apple-native", "Swift/Objective-C or Xcode project evidence")
        if any(p.lower().endswith(".swift") for p in apple_paths):
            languages.add("Swift")
        if any(p.lower().endswith((".m", ".mm")) for p in apple_paths):
            languages.add("Objective-C")
        if any("package.swift" in p.lower() for p in paths):
            build_tools.add("Swift Package Manager")

    # Desktop/game/custom-renderer signals; these do not exclude the families above.
    if any(p.lower().endswith((".csproj", ".sln")) for p in paths):
        add_signal("desktop-dotnet", ".NET project/solution file")
        languages.add("C#")
        build_tools.add("MSBuild/dotnet")
    if any("project.godot" == Path(p).name.lower() for p in paths):
        add_signal("game-engine", "Godot project.godot")
    if any(Path(p).name.lower() in {"unityprojectsettings.asset", "manifest.json"} and "packages/" in p.lower() for p in paths):
        add_signal("game-engine", "Unity package/project asset evidence")
    if any(p.lower().endswith((".glsl", ".vert", ".frag", ".wgsl", ".metal", ".hlsl", ".shader")) for p in paths):
        graphics.add("shader source present (language inferred from extension only)")
    if any(p.lower().endswith((".c", ".cc", ".cpp", ".h", ".hpp")) for p in paths):
        languages.add("C/C++")
        if any(p.lower().endswith("cmakelists.txt") for p in paths):
            build_tools.add("CMake")

    for family, items in sorted(evidence.items()):
        confidence = "high" if len(items) >= 2 and (family != "android-native" or android_manifest and gradle_paths) else "medium"
        candidates.append({"family": family, "confidence": confidence, "evidence": sorted(set(items))})

    if not evidence:
        candidates.append({"family": "unknown", "confidence": "low", "evidence": ["No recognized project markers found"]})

    return {
        "root": str(root),
        "files_sampled": len(paths),
        "file_limit_reached": len(paths) >= MAX_FILES,
        "languages": sorted(languages),
        "build_tools": sorted(build_tools),
        "graphics_signals": sorted(graphics),
        "platform_candidates": candidates,
        "minimum_android_sdk_observed": min_sdk,
        "sample_paths": paths[:80],
        "limitations": [
            "Heuristic file inventory only; inspect source imports, build configuration, and runtime behavior before making decisions.",
            "No renderer is recommended and no source files are modified.",
            "Missing markers do not prove a platform or graphics capability is absent."
        ]
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", help="Path to the project root to inspect (read-only)")
    args = parser.parse_args()
    try:
        result = inspect(args.project_root)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
