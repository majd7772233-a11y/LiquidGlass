# Install Liquid Glass for Codex

This is a repository-local Agent Skill at `.agents/skills/liquid-glass/`. Current Codex guidance documents `.agents/skills/` for project skills and `~/.agents/skills/` for personal skills. A skill is discovered from its folder and required `SKILL.md` metadata; its optional references, scripts, and examples travel with the folder.

## Use it in this repository

Open this repository (or a subdirectory beneath it) in Codex. The skill is located at:

```text
.agents/skills/liquid-glass/SKILL.md
```

Invoke it explicitly with `$liquid-glass`, or describe a matching implementation/review task so Codex can consider it for implicit invocation. Skill discovery does not guarantee that an agent will invoke it for every related prompt.

## Install it for all your projects

### Windows PowerShell

```powershell
# Clone the public repository if you do not already have it.
git clone https://github.com/majd7772233-a11y/LiquidGlass.git

$skillsHome = Join-Path $HOME ".agents\skills"
New-Item -ItemType Directory -Force -Path $skillsHome | Out-Null
$target = Join-Path $skillsHome "liquid-glass"
if (Test-Path $target) { Remove-Item -LiteralPath $target -Recurse -Force }
Copy-Item -Recurse -Force `
  ".\LiquidGlass\.agents\skills\liquid-glass" `
  $target
```

If the repository is already cloned, run only the `New-Item` and `Copy-Item` commands from its parent directory. To update, pull the latest repository changes and repeat the copy command. Back up any local edits in the personal skill folder first; the update command replaces that installed folder.

### macOS / Linux / Git Bash

```bash
git clone https://github.com/majd7772233-a11y/LiquidGlass.git
mkdir -p "$HOME/.agents/skills"
rm -rf "$HOME/.agents/skills/liquid-glass"
cp -R LiquidGlass/.agents/skills/liquid-glass "$HOME/.agents/skills/"
```

To update, pull the latest repository changes and replace the installed `liquid-glass` directory with the newer copy.

## Verify the package

From the repository root:

```bash
python .agents/skills/liquid-glass/scripts/inspect_project.py .
python -m unittest discover -s .agents/skills/liquid-glass/tests -v
```

The inventory script prints evidence only; the tests validate package structure and the bundled workflow fixtures. They do not prove visual parity on a physical device.

If the skill does not appear in an already-running Codex session, start a new session or restart Codex. The skill name must remain `liquid-glass`, matching its directory and `SKILL.md` frontmatter.

## Keep in mind

- Keep the entire skill directory together; do not copy `SKILL.md` without its `references/`, `scripts/`, `examples/`, and `agents/` folders.
- The repository-local copy is updated when this repository is updated. A personal copy must be updated separately.
- For exact supported locations and current behavior, consult the official [Build skills guide](https://learn.chatgpt.com/docs/build-skills).
