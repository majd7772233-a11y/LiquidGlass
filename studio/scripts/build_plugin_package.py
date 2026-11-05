from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

STUDIO_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = STUDIO_ROOT.parent
PACKAGE_SOURCE = STUDIO_ROOT / "package-source"
SKILL_ROOT = Path("skills/liquid-glass-studio")
SKILL_FILE = SKILL_ROOT / "SKILL.md"

# Canonical repository path -> path inside the private plugin's Skill package.
REFERENCE_MAP = {
    ".agents/skills/liquid-glass/SKILL.md": "references/liquid-glass-core.md",
    "studio/tool-contracts.md": "references/tool-contracts.md",
    ".agents/skills/liquid-glass/references/project-discovery.md": "references/project-discovery.md",
    ".agents/skills/liquid-glass/references/rendering-strategy.md": "references/rendering-strategy.md",
    ".agents/skills/liquid-glass/references/visual-contract.md": "references/visual-contract.md",
    ".agents/skills/liquid-glass/references/motion-accessibility-performance.md": "references/motion-accessibility-performance.md",
    ".agents/skills/liquid-glass/references/validation-and-reporting.md": "references/validation-and-reporting.md",
    ".agents/skills/liquid-glass/references/implementation-workflow.md": "references/implementation-workflow.md",
    "docs/visual-specification.md": "references/visual-specification.md",
    "docs/interaction-and-motion.md": "references/interaction-and-motion.md",
    "docs/reference-matrix.md": "references/reference-matrix.md",
    "docs/platform-adaptation/README.md": "references/platform-adaptation/README.md",
    "docs/platform-adaptation/capability-matrix.md": "references/platform-adaptation/capability-matrix.md",
    "docs/platform-adaptation/web.md": "references/platform-adaptation/web.md",
    "docs/platform-adaptation/android.md": "references/platform-adaptation/android.md",
    "docs/platform-adaptation/android-library-catalog.md": "references/platform-adaptation/android-library-catalog.md",
    "docs/platform-adaptation/apple.md": "references/platform-adaptation/apple.md",
    "docs/platform-adaptation/desktop.md": "references/platform-adaptation/desktop.md",
    "docs/platform-adaptation/game-engines.md": "references/platform-adaptation/game-engines.md",
    "docs/platform-adaptation/cross-platform.md": "references/platform-adaptation/cross-platform.md",
    "docs/platform-adaptation/constrained.md": "references/platform-adaptation/constrained.md",
    ".agents/skills/liquid-glass/examples/README.md": "references/workflow-examples/README.md",
    ".agents/skills/liquid-glass/examples/android-java/WORKFLOW.md": "references/workflow-examples/android-java/WORKFLOW.md",
    ".agents/skills/liquid-glass/examples/web-dom/WORKFLOW.md": "references/workflow-examples/web-dom/WORKFLOW.md",
}


def validate_package(root: Path) -> None:
    manifest = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    app = json.loads((root / ".app.json").read_text(encoding="utf-8"))

    if manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
        raise ValueError("Missing Agent Plugins 1.0 schema declaration")
    if manifest.get("name") != "liquid-glass-studio":
        raise ValueError("Plugin name must remain liquid-glass-studio")
    version_parts = manifest.get("version", "").split(".")
    if len(version_parts) != 3 or any(not part.isdigit() for part in version_parts):
        raise ValueError("Plugin version must be strict SemVer")
    openai = manifest.get("extensions", {}).get("com.openai", {})
    interface = openai.get("interface", {})
    if openai.get("apps") != "./.app.json":
        raise ValueError("The GitHub app binding must use the root .app.json")
    if interface.get("displayName") != "Liquid Glass Studio":
        raise ValueError("Unexpected display name")
    if len(interface.get("shortDescription", "")) > 30:
        raise ValueError("Plugin shortDescription exceeds 30 characters")
    if interface.get("category") != "Developer Tools":
        raise ValueError("Plugin category must be Developer Tools")
    if not isinstance(interface.get("capabilities"), list):
        raise ValueError("Plugin capabilities must be an array")
    app_id = app.get("apps", {}).get("github", {}).get("id")
    if app_id != "connector_76869538009648d5b282a4bb21c3d157":
        raise ValueError("Unexpected GitHub connector ID")

    skill_path = root / SKILL_FILE
    skill = skill_path.read_text(encoding="utf-8")
    frontmatter = re.match(r"^---\n(.*?)\n---\n", skill, flags=re.S)
    if not frontmatter:
        raise ValueError("Studio SKILL.md is missing YAML frontmatter")
    if not re.search(r"^name:\s*liquid-glass-studio\s*$", frontmatter.group(1), flags=re.M):
        raise ValueError("Studio Skill name does not match its directory")
    if not re.search(r"^description:\s*\S", frontmatter.group(1), flags=re.M):
        raise ValueError("Studio Skill description is missing")

    for source, destination in REFERENCE_MAP.items():
        staged = root / SKILL_ROOT / destination
        if not staged.is_file():
            raise ValueError(f"Missing packaged reference: {destination} (source {source})")

    link_pattern = re.compile(r"\[[^]]+\]\(([^)]+)\)")
    candidates = [skill_path]
    for markdown_path in candidates:
        source_text = markdown_path.read_text(encoding="utf-8")
        for target in link_pattern.findall(source_text):
            target = target.strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            local = (markdown_path.parent / target.split("#", 1)[0].split("?", 1)[0]).resolve()
            if not local.is_file():
                raise ValueError(f"Broken packaged link: {markdown_path.relative_to(root)} -> {target}")


def build_package(output: Path) -> Path:
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="liquid-glass-studio-") as temporary:
        root = Path(temporary) / "plugin"
        shutil.copytree(PACKAGE_SOURCE, root)
        for source, destination in REFERENCE_MAP.items():
            source_path = REPO_ROOT / source
            if not source_path.is_file():
                raise FileNotFoundError(f"Canonical reference is missing: {source}")
            destination_path = root / SKILL_ROOT / destination
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, destination_path)

        index_path = root / SKILL_ROOT / "references" / "README.md"
        index_path.write_text(
            "# Packaged shared knowledge\n\n"
            "These files are copied at build time from canonical LiquidGlass repository sources. "
            "Do not edit copies directly; update the source and rebuild the plugin.\n",
            encoding="utf-8",
        )
        shutil.copy2(REPO_ROOT / "LICENSE", root / "LICENSE")
        shutil.copy2(REPO_ROOT / "PROVENANCE.md", root / "PROVENANCE.md")
        validate_package(root)
        if output.exists():
            output.unlink()
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(root.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(root).as_posix())
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the private Liquid Glass Studio plugin archive.")
    parser.add_argument("--output", type=Path, default=Path("/tmp/liquid-glass-studio.zip"))
    parser.add_argument("--check", action="store_true", help="Build into a temporary directory and validate.")
    args = parser.parse_args()
    if args.check:
        with tempfile.TemporaryDirectory(prefix="liquid-glass-studio-check-") as temporary:
            result = build_package(Path(temporary) / "liquid-glass-studio.zip")
            print(f"Validated {result.stat().st_size} bytes")
        return 0
    print(build_package(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
