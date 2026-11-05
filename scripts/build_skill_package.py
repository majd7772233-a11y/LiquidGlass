from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_SOURCE = REPO_ROOT / ".agents" / "skills" / "liquid-glass"
DOCS_SOURCE = REPO_ROOT / "docs"
PACKAGE_NAME = "liquid-glass"
REPOSITORY_URL = "https://github.com/majd7772233-a11y/LiquidGlass"
LINK_PATTERN = re.compile(r"(!?\[[^\]]*\]\()([^)]+)(\))")
SEMVER_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def rewrite_markdown_links(source_file: Path, package_file: Path, package_root: Path) -> None:
    source_text = source_file.read_text(encoding="utf-8")

    def replace_link(match: re.Match[str]) -> str:
        original = match.group(2).strip()
        if original.startswith("<") and original.endswith(">"):
            original = original[1:-1]
        parsed = urlsplit(original)
        if parsed.scheme or original.startswith(("#", "/")) or not parsed.path:
            return match.group(0)

        source_target = (source_file.parent / unquote(parsed.path)).resolve()
        package_target: Path | None = None

        try:
            docs_relative = source_target.relative_to(DOCS_SOURCE.resolve())
            package_target = package_root / "references" / "project-docs" / docs_relative
        except ValueError:
            try:
                skill_relative = source_target.relative_to(SKILL_SOURCE.resolve())
                package_target = package_root / skill_relative
            except ValueError:
                try:
                    repository_relative = source_target.relative_to(REPO_ROOT.resolve())
                except ValueError:
                    return match.group(0)
                remote_url = REPOSITORY_URL + "/blob/main/" + repository_relative.as_posix()
                if parsed.query:
                    remote_url += "?" + parsed.query
                if parsed.fragment:
                    remote_url += "#" + parsed.fragment
                return match.group(1) + remote_url + match.group(3)

        relative_target = posixpath.relpath(
            package_target.as_posix(),
            package_file.parent.as_posix(),
        )
        if parsed.query:
            relative_target += "?" + parsed.query
        if parsed.fragment:
            relative_target += "#" + parsed.fragment
        return match.group(1) + relative_target + match.group(3)

    package_file.write_text(LINK_PATTERN.sub(replace_link, source_text), encoding="utf-8")


def validate_markdown_links(package_root: Path) -> None:
    for markdown_file in package_root.rglob("*.md"):
        content = markdown_file.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(content):
            target = match.group(2).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith(("/", "#")) or not parsed.path:
                continue
            resolved = (markdown_file.parent / unquote(parsed.path)).resolve()
            if not resolved.exists():
                raise ValueError(
                    "Broken package link: "
                    + str(markdown_file.relative_to(package_root))
                    + " -> "
                    + target
                )


def validate_package(package_root: Path) -> dict[str, object]:
    version = (package_root / "VERSION").read_text(encoding="utf-8").strip()
    if not SEMVER_PATTERN.fullmatch(version):
        raise ValueError("Skill VERSION must be strict SemVer (major.minor.patch).")

    skill_file = package_root / "SKILL.md"
    if not skill_file.is_file():
        raise ValueError("Package entry point SKILL.md is missing.")
    if not (package_root / "scripts" / "install.ps1").is_file():
        raise ValueError("PowerShell installer is missing.")
    if not (package_root / "scripts" / "uninstall.ps1").is_file():
        raise ValueError("PowerShell uninstaller is missing.")
    if not (package_root / "LICENSE").is_file() or not (package_root / "PROVENANCE.md").is_file():
        raise ValueError("License and provenance notices must accompany the package.")

    frontmatter = skill_file.read_text(encoding="utf-8")
    if not frontmatter.startswith("---\n") or not re.search(r"^name:\s*liquid-glass\s*$", frontmatter, re.M):
        raise ValueError("Skill frontmatter name does not match liquid-glass.")

    validate_markdown_links(package_root)
    return {
        "schema_version": 1,
        "name": PACKAGE_NAME,
        "version": version,
        "entrypoint": "SKILL.md",
        "source_repository": REPOSITORY_URL,
        "package_policy": {
            "self_contained_project_docs": True,
            "user_supplied_visual_references_included": False,
            "private_plugin_binding_included": False,
        },
    }


def build_package(output: Path) -> Path:
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="liquid-glass-skill-") as temporary:
        staging_root = Path(temporary) / PACKAGE_NAME
        shutil.copytree(SKILL_SOURCE, staging_root)
        shutil.copytree(DOCS_SOURCE, staging_root / "references" / "project-docs")
        shutil.copy2(REPO_ROOT / "LICENSE", staging_root / "LICENSE")
        shutil.copy2(REPO_ROOT / "PROVENANCE.md", staging_root / "PROVENANCE.md")
        shutil.copy2(REPO_ROOT / "CHANGELOG.md", staging_root / "CHANGELOG.md")

        for package_file in staging_root.rglob("*.md"):
            relative = package_file.relative_to(staging_root)
            if relative.parts[:2] == ("references", "project-docs"):
                source_file = DOCS_SOURCE / Path(*relative.parts[2:])
            else:
                source_file = SKILL_SOURCE / relative
            if not source_file.is_file():
                raise FileNotFoundError("No canonical source for " + str(relative))
            rewrite_markdown_links(source_file, package_file, staging_root)

        manifest = validate_package(staging_root)
        file_hashes: dict[str, str] = {}
        for path in sorted(staging_root.rglob("*")):
            if path.is_file() and path.name != "manifest.json":
                file_hashes[path.relative_to(staging_root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        manifest["sha256"] = file_hashes
        (staging_root / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        if output.exists():
            output.unlink()
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(staging_root.rglob("*")):
                if not path.is_file():
                    continue
                relative = (Path(PACKAGE_NAME) / path.relative_to(staging_root)).as_posix()
                info = zipfile.ZipInfo(relative, date_time=(2024, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (0o100644 & 0xFFFF) << 16
                archive.writestr(info, path.read_bytes())

    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a self-contained, versioned Liquid Glass Skill ZIP.")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check", action="store_true", help="Build and validate in a temporary directory.")
    args = parser.parse_args()

    version = (SKILL_SOURCE / "VERSION").read_text(encoding="utf-8").strip()
    output = args.output or (REPO_ROOT / "dist" / (PACKAGE_NAME + "-skill-" + version + ".zip"))

    if args.check:
        with tempfile.TemporaryDirectory(prefix="liquid-glass-skill-check-") as temporary:
            result = build_package(Path(temporary) / "skill.zip")
            print("Validated " + str(result.stat().st_size) + " bytes")
        return 0

    print(build_package(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
