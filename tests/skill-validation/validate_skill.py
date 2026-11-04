#!/usr/bin/env python3
"""Validate the Liquid Glass Codex Skill package and workflow fixtures."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / ".agents" / "skills" / "liquid-glass"
SKILL_FILE = SKILL_DIR / "SKILL.md"
REQUIRED_FILES = (
    SKILL_FILE,
    SKILL_DIR / "agents" / "openai.yaml",
    SKILL_DIR / "references" / "project-discovery.md",
    SKILL_DIR / "references" / "technique-selection.md",
    SKILL_DIR / "references" / "material-and-motion.md",
    SKILL_DIR / "references" / "implementation-workflow.md",
    SKILL_DIR / "references" / "quality-validation.md",
    SKILL_DIR / "assets" / "implementation-brief.template.md",
    SKILL_DIR / "assets" / "visual-review.template.md",
    ROOT / "docs" / "skill-installation.md",
)
EXPECTED_STAGES = ["discover", "specify", "select", "plan", "implement", "validate", "report"]
SCENARIO_DIR = ROOT / "tests" / "skill-validation" / "scenarios"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_files() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_FILES if not path.is_file()]
    if missing:
        fail("missing required package files: " + ", ".join(missing))
    print("PASS: required Skill, reference, template, metadata, and installation files exist")


def read_skill_metadata() -> str:
    text = SKILL_FILE.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must begin with YAML front matter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        fail("SKILL.md front matter is not closed")
    front = parts[1]
    name_match = re.search(r"^name:\s*([a-z0-9-]+)\s*$", front, re.MULTILINE)
    description_match = re.search(r'^description:\s*"(.+)"\s*$', front, re.MULTILINE)
    if not name_match or name_match.group(1) != "liquid-glass":
        fail("Skill name must be exactly 'liquid-glass'")
    if not description_match:
        fail("Skill description must be a single quoted YAML string")
    description = description_match.group(1)
    if not 50 <= len(description) <= 1024:
        fail("Skill description length must be between 50 and 1024 characters")
    print("PASS: Codex Skill front matter, name, and description")
    return text


def check_metadata_yaml() -> None:
    metadata = (SKILL_DIR / "agents" / "openai.yaml").read_text(encoding="utf-8")
    for required in ("interface:", "display_name:", "short_description:", "default_prompt:", "policy:", "allow_implicit_invocation: true"):
        if required not in metadata:
            fail(f"agents/openai.yaml is missing {required}")
    print("PASS: optional agents/openai.yaml interface and invocation metadata")


def markdown_files():
    yield from SKILL_DIR.rglob("*.md")
    yield ROOT / "docs" / "skill-installation.md"
    yield ROOT / "tests" / "skill-validation" / "README.md"


def check_local_markdown_links() -> None:
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    errors = []
    for path in markdown_files():
        source = path.read_text(encoding="utf-8")
        for destination in pattern.findall(source):
            destination = destination.strip()
            if not destination or destination.startswith(("#", "https://", "http://", "mailto:")):
                continue
            destination = destination.split("#", 1)[0].split("?", 1)[0]
            if not destination:
                continue
            target = (path.parent / destination).resolve()
            if not target.exists():
                errors.append(f"{path.relative_to(ROOT)} -> {destination}")
    if errors:
        fail("broken local Markdown links: " + "; ".join(errors))
    print("PASS: all local Markdown links in Skill and test/install docs resolve")


def check_scenarios() -> None:
    scenarios = sorted(SCENARIO_DIR.glob("*.json"))
    if len(scenarios) < 2:
        fail("at least two platform workflow scenario fixtures are required")
    families = set()
    all_skill_text = " ".join(path.read_text(encoding="utf-8").lower() for path in SKILL_DIR.rglob("*.md"))
    for path in scenarios:
        try:
            scenario = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            fail(f"invalid scenario {path.name}: {exc}")
        required_keys = ("id", "platform_family", "project_profile", "task", "must_discover", "must_consider", "must_not_assume", "workflow", "acceptance", "required_skill_terms")
        for key in required_keys:
            if key not in scenario:
                fail(f"{path.name} is missing required key: {key}")
        families.add(scenario["platform_family"])
        stages = [step.get("stage") for step in scenario["workflow"] if isinstance(step, dict)]
        if stages != EXPECTED_STAGES:
            fail(f"{path.name} workflow stages must be ordered as: {', '.join(EXPECTED_STAGES)}")
        if any(not step.get("required_output") for step in scenario["workflow"]):
            fail(f"{path.name} contains a workflow stage without a required output")
        if len(scenario["must_discover"]) < 4 or len(scenario["acceptance"]) < 3:
            fail(f"{path.name} does not contain enough discovery/acceptance criteria")
        missing_terms = [term for term in scenario["required_skill_terms"] if term.lower() not in all_skill_text]
        if missing_terms:
            fail(f"{path.name} required terms not covered by Skill references: {', '.join(missing_terms)}")
    if len(families) < 2:
        fail("workflow fixtures must cover at least two distinct platform families")
    if any(json.loads(p.read_text(encoding="utf-8"))["workflow"][-1]["stage"] != "report" for p in scenarios):
        fail("each workflow must end with a report stage")
    print(f"PASS: {len(scenarios)} end-to-end workflow fixtures across {len(families)} platform families ({', '.join(sorted(families))})")


def main() -> None:
    check_files()
    read_skill_metadata()
    check_metadata_yaml()
    check_local_markdown_links()
    check_scenarios()
    print("RESULT: all Liquid Glass Skill package checks passed")


if __name__ == "__main__":
    main()
