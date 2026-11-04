# Studio architecture and twin contract

## 1. Two execution environments, one core

| Concern | Codex twin | ChatGPT Studio twin |
|---|---|---|
| Invocation | `$liquid-glass` | `@Liquid Glass Studio` |
| Project access | Local workspace, files, shell, build tools available to Codex | GitHub repository and Actions through the bound GitHub connector |
| Reference input | Local/attached screenshots and video frames | Chat attachments and supplied screenshots/video frames |
| Implementation | Direct local file edits and local commands | GitHub file/tree/commit operations on the authorized repository |
| Verification | Local tests, builds, emulator/device, screenshots | GitHub Actions, repository checks, and supplied captures; no claim of local device access |
| Shared standard | Repository visual specs, L0–L3, platform matrices, Android fallback rules | Same source documents packaged into the Studio Skill |

The agent must inspect the target before choosing an implementation. The execution adapters cannot silently change the design standard.

## 2. Knowledge source and synchronization

Canonical shared knowledge remains in the repository:

- `.agents/skills/liquid-glass/SKILL.md` and its references;
- `docs/visual-specification.md`, `docs/interaction-and-motion.md`, and `docs/reference-matrix.md`;
- `docs/platform-adaptation/` including the Android dependency catalog;
- platform workflow fixtures under `.agents/skills/liquid-glass/examples/`.

The Studio package builder copies these files into the plugin's `references/` folder. Tests ensure all mapped sources exist, package links resolve, the Skill and manifest are valid, and the GitHub binding points to the verified connector ID. Update canonical knowledge first, rebuild and test the plugin package, then update the private plugin release. This keeps the twins aligned without requiring a network lookup of the LiquidGlass repository for every unrelated target project.

## 3. GitHub execution adapter

The plugin declares the existing GitHub connector in `.app.json`. Studio maps its workflows onto the host GitHub actions:

- discovery: repository metadata, branch refs, tree listings, file reads, and code search;
- editing: create/update files, or create blobs → tree → commit → guarded ref update;
- review: fetch current files, diffs, PR metadata, comments, and changed paths;
- verification: inspect workflow runs, jobs, job logs, and commit status.

For multi-file work, prefer an isolated branch and an atomic commit when feasible. Follow the user's explicit branch/PR preference. Never force-push or overwrite unrelated changes. Verify the target branch head after writing and verify CI against the exact resulting commit.

## 4. Authorization and safety boundaries

- Read-only analysis does not change project files.
- `implement_glass` performs writes only when the user explicitly requests implementation, adaptation, fixing, or another change.
- Limit writes to the named repository, branch, feature scope, and files needed for that task.
- Ask before destructive deletion, history rewriting, force-push, credential/secret changes, permission changes, or scope expansion.
- Do not copy secrets into chat, logs, plugin files, or commits.
- Never claim a build/test/device run based solely on a successful commit or on CI being queued.
- When GitHub cannot access a repository or a required action, report the exact boundary; do not fabricate a local or remote execution.

## 5. What Studio is not

Studio is not a general-purpose repository host, a local filesystem bridge, a native rendering engine, or an extension that changes ChatGPT's own UI. It is an execution-oriented assistant workflow whose actions depend on the connected GitHub app. It cannot produce real backdrop refraction in a target application merely by describing it: it must modify that application's actual renderer and verify the result to the extent the connected environment permits.

## 6. Hosting choice

The Sites MCP server reference required by the default Sites-hosted creation path was not available in this environment. The supported private package path is therefore used instead: a standalone private Skill package bound to the already-connected GitHub app. No unverified endpoint, Cloudflare Worker, or duplicate server is introduced. Studio uses the host GitHub connector rather than a separately deployed set of custom MCP endpoints.
