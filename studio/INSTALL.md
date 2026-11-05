# Liquid Glass Studio — setup and updates

Liquid Glass Studio is a **private personal ChatGPT plugin**, not a public
plugin-directory package. The existing personal installation is version 0.1.0,
has the verified GitHub connector binding, and has already been exercised with
the @Liquid Glass Studio invocation.

## Open and use the existing installation

[Open Liquid Glass Studio in ChatGPT](https://chatgpt.com/plugins/plugins_6aeb5696483c81919fbad78423d2767e).

In a new chat, invoke it with @Liquid Glass Studio and give it a concrete
repository task. The existing GitHub connector must be connected and authorized
for the repository being changed. Studio works through that GitHub connection;
it does not have access to local files, local emulators, or the user's physical
devices.

If the link is unavailable in a different account, do not assume the public
repository can recreate the same private account object. The private plugin
must be created or enabled through the supported plugin workflow for that
account, with the GitHub connector explicitly bound and authorized.

## Rebuild after changing shared knowledge

Canonical Studio source is under package-source/; canonical Skill and platform
guidance remain in the repository's Skill and docs directories.

From the repository root:

    python studio/scripts/build_plugin_package.py --check
    python studio/scripts/build_plugin_package.py --output dist/liquid-glass-studio-private.zip
    python -m unittest discover -s studio/tests -v

The builder validates the package layout, manifest, Skill references, and the
existing GitHub connector ID. The archive includes .app.json and is therefore
private/account-bound. Never upload it as a public plugin or attach it to a
public source release.

When preparing a private update, bump the version in package-source/plugin.json,
rebuild and test the archive, then use the supported private plugin
authoring/update flow for the account. Confirm the updated version and test
@Liquid Glass Studio in ChatGPT. Building this ZIP does not itself update the
already-installed private plugin. Keep the package version aligned with the
standalone Skill version for coordinated releases.

## Connection and privacy boundary

The GitHub app binding identifies the existing connector; it is not an access
token. Repository permissions remain controlled by the user's connected
GitHub account. Do not place tokens, secrets, local file paths, or device
identifiers in the manifest or package.
