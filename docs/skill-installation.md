# Installing and Updating the Liquid Glass Skill

## ChatGPT Desktop for Windows (Microsoft Store)

For the ChatGPT Desktop Microsoft Store setup used by the maintainer, the personal Codex Skills directory is:

`$HOME\.codex\skills\`

For the current Windows profile, that is:

`C:\Users\Magd\.codex\skills\`

The installed Skill path is:

`%USERPROFILE%\.codex\skills\liquid-glass\SKILL.md`

**Do not use `%USERPROFILE%\.agents\skills` as the personal install destination for this ChatGPT Desktop setup.** The repository-local directory described below is different.

Follow the complete [Windows ChatGPT Desktop installation guide](../.agents/skills/liquid-glass/INSTALL.md). It includes a PowerShell installer/updater that checks the source, backs up an existing personal copy, copies the entire Skill, and verifies the result.

## Repository-local installation

The version-controlled Skill remains at [`.agents/skills/liquid-glass/`](../.agents/skills/liquid-glass/SKILL.md). Keep that directory in this repository. This is the project copy; it is not the personal destination used by the ChatGPT Desktop Store installation above.

## Update

1. Pull the latest repository changes with `git pull --ff-only`.
2. From the repository root, rerun the PowerShell block in [INSTALL.md](../.agents/skills/liquid-glass/INSTALL.md).
3. Restart ChatGPT Desktop or start a new Codex session.
4. Invoke the Skill explicitly with `$liquid-glass`.

The installer backs up the existing `liquid-glass` folder before replacing it. It does not remove or modify neighboring Skills.

## Validate the Skill package

From the repository root:

```powershell
python .agents/skills/liquid-glass/scripts/inspect_project.py .
python -m unittest discover -s .agents/skills/liquid-glass/tests -v
```

The inventory helper is read-only. The package tests validate metadata, local references, platform-discovery fixtures, and the documented platform guidance. They do not replace target-app builds or visual testing on physical hardware.

## Client-specific paths

The `.codex\skills` path above is documented specifically for the maintainer ChatGPT Desktop Microsoft Store environment. Do not generalize it to every Codex distribution without checking that client actual Skills directory.
