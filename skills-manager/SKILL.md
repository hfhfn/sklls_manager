---
name: skills-manager
description: "Wire the skills-manager desktop app to agent skills dirs."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [skills-manager, skills, hermes, agent-tools, presets, junction, integration]
    related_skills: [hermes-agent, cc-switch]
---

# skills-manager (agent skills integration)

> **User boundary (IMPORTANT):** Do NOT manage skills-manager's sync strategy on your own.
> The user decides which skills get synced to which agent. Only run `install`/`sync`/`add-skill`
> when the user explicitly asks. This includes not proactively syncing newly installed skills
> to every agent — sync only what the user requests.

`skills-manager` is a Tauri desktop app (Windows) that centrally manages agent skills and syncs them into many coding agents' skills directories. It ships a shared-core CLI that mirrors the GUI and shares the same SQLite DB. Its central repo lives at `~/.skills-manager/` and the binaries at `AppData\Local\skills-manager\`.

On this host the GUI app is `skills-manager.exe` and the CLI is `skills-manager-cli.exe` (both under `C:\Users\hfhfn\AppData\Local\skills-manager\`). The GUI shares the same DB as the CLI, so CLI changes show up in the GUI on next refresh.

## How agent detection works (the key gotcha)

skills-manager has a **built-in registry of tool definitions** (including `hermes`, `claude_code`, `codex`, `opencode`, `github_copilot`, and many more). Each tool definition has a **hardcoded default `skills_dir`**. The tool reports `installed: true` **only if that default skills directory exists on disk**. If the directory is missing, it reports `installed: false` and skills are not offered for sync.

Check per-tool status (from the CLI dir):

```bash
cd /c/Users/hfhfn/AppData/Local/skills-manager
./skills-manager-cli.exe tools list --json \
  | python -c "import sys,json; d=json.load(sys.stdin); [print(json.dumps(t,ensure_ascii=False)) for t in d if t['key']=='hermes']"
```

The Hermes tool definition defaults to `~/.hermes/skills`. If your real Hermes home is elsewhere (`$HERMES_HOME`, e.g. `AppData\Local\hermes`), that default path does not exist → Hermes shows `installed: false` even though Hermes is fully installed. **This is the #1 reason Hermes is "not detected."**

## Fix for non-default HERMES_HOME: directory junction

Bridge the hardcoded default to the real Hermes skills dir with a directory junction (works without admin; `os.symlink(..., target_is_directory=True)` is more reliable than `cmd mklink` from git-bash):

```python
import os
os.symlink(r'C:\Users\hfhfn\AppData\Local\hermes\skills',
           r'C:\Users\hfhfn\.hermes\skills', target_is_directory=True)
```

Verify and re-check detection:

```bash
python -c "import os; print(os.path.islink(r'C:\Users\hfhfn\.hermes\skills'))"
# Hermes tool should now show installed: true
```

The junction itself does NOT copy anything — it makes the tool's default path resolve to the real dir. This is safe and additive; existing Hermes skills stay put.

## Central copy vs agent-local copy can be the SAME physical dir (verify by inode)

A skill that appears under both the central repo `~/.skills-manager/skills/<name>/` and an
agent's real skills dir (e.g. `AppData\Local\hermes\skills\<name>\`) may be the **same physical
directory** rather than two copies — common for locally-authored/edited skills (not registry-installed
ones). Before assuming a re-sync is needed, compare inodes:

```bash
stat -c%i ~/.skills-manager/skills/video2markdown/SKILL.md \
            /c/Users/hfhfn/AppData/Local/hermes/skills/video2markdown/SKILL.md
# identical number → same physical file
```

Same inode means the central entry resolves to the agent's source dir (junction/symlink or literally
the same path): **edits to the source already hit the central repo and every synced agent automatically —
no `skills sync`, no copy, no re-sync.** Verify end-to-end by confirming a newly added file (e.g. a
`references/*.md`) shows the same inode in both places, and that the CLI still lists the skill
(`skills-manager-cli.exe skills list --json`). Only when inodes differ (genuine separate copies, e.g. a
registry-installed skill duplicated into the repo) does an explicit sync actually matter.

## Adopting a locally-authored Hermes skill (`skills adopt`)

When you *create* a skill directly in Hermes (via `skill_manage create`, e.g. under
`AppData\Local\hermes\skills\<category>\<name>`) and want it tracked in the central repo, use
`skills adopt <skill-dir>` — NOT `install` (that's for registry/git refs). This came up when a
`memory-curation` skill created this way needed to reach skills-manager.

```bash
cd /c/Users/hfhfn/AppData/Local/skills-manager

# dry-run first (confirms the dir is recognized as adoptable)
./skills-manager-cli.exe skills adopt \
  "C:\Users\hfhfn\AppData\Local\hermes\skills\devops\memory-curation" --dry-run --json
# {"ok":true,"candidates":[{"path":"...","name":"memory-curation","reason":"ready"}],"skipped":[]}

# real adopt
./skills-manager-cli.exe skills adopt \
  "C:\Users\hfhfn\AppData\Local\hermes\skills\devops\memory-curation" --json
# {"ok":true,"adopted":[{"ok":true,"skill_id":"<uuid>","name":"memory-curation",
#   "central_path":"...\skills\memory-curation","source_type":"local","synced":false,"preset_id":null}]}
```

Key semantics (verify with `skills list --json` after):
- Adopt **copies** the skill into `~/.skills-manager/skills/<name>/` as a NEW separate physical dir,
  recording `source_type:"local"` and `source_ref` = your Hermes source path. Unlike the junction/same-inode
  case above, adopt creates **two real copies**: later edits to the Hermes source do NOT auto-propagate to
  the central copy. If you keep editing the source, re-adopt or edit the central copy.
- Adopt result state is `enabled:true, presets:[], deployed_to:[], preset_id:null`. It does **NOT** add the
  skill to any preset nor deploy it to any agent. That is the user's call (per the boundary rule at top) —
  confirm with the user before adding to a preset / deploying, unless they already asked.
- The adopted skill stays usable by Hermes directly from its own source dir (source_ref), independent of
  any skills-manager deployment.

## Syncing skills into an agent

```bash
# dry-run first (lists what would be sync'd, all symlink mode)
./skills-manager-cli.exe skills sync --tool hermes --dry-run

# real sync of the active preset into Hermes
./skills-manager-cli.exe skills sync --tool hermes
```

Sync creates **symlinks** in the target agent skills dir pointing back into `~/.skills-manager/skills/<name>` — read-only, additive, does not copy or clobber existing skills. Deleting a skill in skills-manager breaks its symlinks in every synced agent (that's the "unified management" design, expected).

## Installing a skill by owner/repo (subdir resolution)

`skills install <REFERENCE>` where REFERENCE is `owner/repo` or `owner/repo/skill-name`:
- Without `--git`, it goes through the **skills.sh registry**: clones the repo into
  `~/.skills-manager/cache/repos/<hash>`, then finds the skill **by its directory name**
  under the repo (e.g. `skills/<skill-name>/` with a `SKILL.md`).
- Error `Skill '<name>' not found in ...Temp\skills-manager-clone-<hash>` means the repo
  was cloned but **no directory named `<name>` exists in it**. This is a skills.sh index
  staleness bug: the registry advertises a skill name that doesn't match the repo's real
  skill dir. Fix: `skills search <term>`, inspect the actual repo (or `git clone` it) to
  find the real skill dir name, then install with that name instead.
- `--git <URL>` treats the whole arg as a git repo URL (appends `.git`) — it does NOT do
  subdir lookup, so `--git owner/repo/skill` fails with 404. Use bare `owner/repo/skill`.
- **skills.sh registry packages ONLY `skills/<name>/` — root-level executables are silently
  dropped.** Toolkits whose CLIs live at the repo root (e.g. `bin/glance` + `vision_client.py`
  alongside `skills/vision-tools/`; a top-level `bin/` of shell/python CLIs) install "successfully"
  but the SKILL.md references commands that don't exist in the central dir. The install reports
  `ok:true` and syncs symlinks, so nothing looks wrong until you run the tool and get
  `command not found`. **Diagnose**: after install, `ls ~/.skills-manager/skills/<name>/` and cross-check
  every command/script the SKILL.md invokes against what's actually there. **Fix**: `mkdir -p bin` and
  `curl` the missing root modules + bin wrappers from `raw.githubusercontent.com/<owner>/<repo>/main/...`
  into the central dir (e.g. `vision_client.py`, `ground.py`, `detect.py` at skill root, `bin/glance` etc.).
  Because syncs are symlinks back to the central dir, adding files there propagates to every synced agent
  with no re-sync. Always `python -m py_compile` the pulled files and end-to-end test one CLI against a
  throwaway image before declaring done.

## Installing a raw git repo (non-skills.sh / non-standard structure)

`skills install <git-URL> --name <name>` pulls a repo directly by URL. Two gotchas:
- **Without `--name`, the skill is registered under a random clone name**
  (`skills-manager-clone-<hash>`), which is useless as a skill name. Always pass
  `--name <desired>` for git-URL installs.
- If install created a junk-named skill before you noticed, remove it and re-install:
  `skills remove skills-manager-clone-<hash> -y` then `skills install <URL> --name <name>`.
- Repos that are **not** standard skills.sh layout (no `skills/<name>/SKILL.md` — e.g. a
  lone `vision.js` + `CLAUDE.md` + `README.md`) install fine but Hermes won't recognize
  them as skills until you add a standard `SKILL.md` (YAML frontmatter with `name`,
  `description`) into the central dir `~/.skills-manager/skills/<name>/SKILL.md`. Because
  syncs are symlinks back to the central dir, editing the central copy propagates to all
  synced agents automatically.
- **Adapting a helper script to the host's vision provider**: such scripts often hardcode
  a third-party default (e.g. DashScope/qwen). Point them at the host's existing vision
  model instead — read the model/base_url/key-env from the Hermes `config.yaml`
  `auxiliary.vision` block (here: Zhipu GLM-4.6V-Flash at `https://open.bigmodel.cn/api/paas/v4`,
  key in `CUSTOM_GLM_API_KEY`). Prefer env-var fallbacks in the script
  (`process.env.VISION_MODEL || "GLM-4.6V-Flash"`, key falls back to the Hermes env var)
  rather than hardcoding the key into the file. Verify end-to-end with a throwaway image
  (tempfile PNG → run the script → expect a real description, not a 429/placeholder).

## skills.sh install may drop the repo's root-level CLIs (multi-file toolkit gotcha)

When a repo is a **multi-file toolkit** (root-level `bin/` CLIs + shared client modules
like `vision_client.py`, plus a `skills/<name>/` subdir), `skills install owner/repo/skill`
via the skills.sh registry only copies the **`skills/<name>/` directory** — it does NOT
bring the root-level `.py` engines and `bin/` executables the skill's SKILL.md references.
Result: the skill installs cleanly and shows no error, but every CLI (`glance`, `ground`,
`detect`, `trace`, `crop`, …) is missing at runtime, and SKILL.md's "If a command is not
found, the optional tools were not installed" note just misleads.

Real case: `Anionex/agent-vision-toolkit` → `vision-tools`. After install, the central dir
had `SKILL.md` + `scripts/` + `references/` + `agents/` + `work/` but **no `bin/` and no
`vision_client.py`/`ground.py`/`detect.py`** at root. The `scripts/*.py` (long_screenshot_ocr,
dominant_colors, pixel_diff, html_shot, extract_fg) came through, but the 5 core CLIs did not.

Fix checklist (do this after any such install, before declaring success):
1. **Diff skill dir vs repo tree.** List the GitHub repo contents
   (`curl .../contents/` and `.../contents/bin` via the local proxy) and compare against
   what `skills install` actually placed under `~/.skills-manager/skills/<name>/`.
2. **Fetch the missing files** into the central skill dir with `curl` through the proxy
   (`https://raw.githubusercontent.com/<owner>/<repo>/main/<path>`), preserving layout —
   root `.py` engines at the skill root, CLIs under `bin/`.
3. **Check imports/relative paths.** The `bin/*` CLIs use `sys.path.insert(0, parents[1])`
   to import the root engine, so root + bin must sit at the same level in the skill dir.
4. **Syntax-check every file** (`python -m py_compile <each>`); confirm runtime deps
   (PIL/numpy/etc.) are installed on the host.
5. **Write the skill's own `.env`** if the client reads one. `agent-vision-toolkit`'s
   `vision_client.load_default_env()` picks up the `.env` **in the skill's own directory**
   (`Path(__file__).parent/.env`) among its candidates — put the config there so it works
   from any cwd. Point it at the host's vision provider (Zhipu GLM, key `CUSTOM_GLM_API_KEY`).
6. **End-to-end verify with a real API call** on a throwaway image — expect a real
   description, not a missing-command crash or a 429. Also smoke-test the local-only CLIs
   (`crop`/`ground`) since they don't need the API.
7. Since syncs are **symlinks back to the central dir**, editing the central copy (adding
   `.env`, `bin/`, engines) propagates to every synced agent automatically — no re-sync needed.

## API keys: skills-manager does NOT manage them

skills-manager has **no key/secret/credential management** — only `repo / tools / skills / presets / git`. It copies skill *files* into each agent's skills dir; it never stores or injects API keys. Keys must be supplied by each agent when it runs a skill.

Each agent reads keys from a *different* place, so there is no "put the key in skills-manager and every agent inherits it" switch:

| Agent | Where it reads keys |
|-------|--------------------|
| Hermes | `~/.hermes/.env` (+ `config.yaml` provider env refs) |
| Claude Code | `~/.claude/settings.json` `env` block, or process env |
| Codex | process env (empty `~/.codex/config.toml` by default) |
| opencode | process env |

**The unified multi-agent pattern** (user's preferred approach): write keys to the **Windows user-level environment** (`HKCU\Environment`) via python+winreg, then broadcast `WM_SETTINGCHANGE` so new processes pick them up. Any agent launched from the user session inherits them — no per-agent config. This is how the GLM key and Brave key are shared across Hermes/Claude Code/Codex/opencode.

```python
import winreg, ctypes
k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE)
for name, val in {"BRAVE_SEARCH_API_KEY": "...", "CUSTOM_GLM_API_KEY": "..."}.items():
    winreg.SetValueEx(k, name, 0, winreg.REG_SZ, val)
winreg.CloseKey(k)
ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001A, 0, "Environment", 0x0002, 5000, None)
```

Verify a fresh process sees them (a git-bash shell won't re-read the registry mid-session — check via a python `winreg` read, or a newly spawned process). Note: `curl` from git-bash can fail to reach some APIs (HTTP 000) where python `urllib` succeeds — when a key "doesn't work", retry with python before blaming the key.

Note: this is a naming convention, not a standard. The skill must reference the env var name it actually expects (e.g. `web-search`/Brave expects `BRAVE_SEARCH_API_KEY`; `claude-vision-skill` reads `CUSTOM_GLM_API_KEY`).

**Renaming one of these shared env vars** (e.g. `HERMES_CUSTOM_GLM_API_KEY` → `CUSTOM_GLM_API_KEY`) must touch every location: Hermes `.env`, `config.yaml` `key_env:` entries, `HKCU\Environment` (set new + delete old + broadcast), the central skill files that read it, and this doc. Full checklist + fresh-subprocess verification pattern: `references/rename-shared-env-key.md`.

## Presets & agents: the pairing model (core of the app)

skills-manager's mental model is **preset ↔ agent pairing**. A **preset** is a named collection of skills (e.g. `Default`, `办公`, `ppt`, `Hermes`). Each agent tool (hermes, claude_code, codex, opencode, …) is paired with a preset; the pairing decides which skills are enabled/synced to that agent. The GUI (and `presets list`/`presets apply`/`presets add-skill`) manages these pairings — that is how you decide which skills go to which agent.

Key commands:
- `presets list` / `presets current` — show presets, counts, and which is active.
- `presets apply <ref>` — switch the active preset (active preset is what a bare `skills sync` uses).
- `presets add-skill / remove-skill <preset> <skill>...` — toggle a skill in a preset.
- `presets preview <preset>` — show what syncing that preset would create (per-skill per-agent target paths).
- `skills sync --preset <p> --tool <t>` — materialize a specific preset→agent pairing (create symlinks).
- `skills sync` (no flags) — sync the **active** preset to all enabled agents.

A skill is "enabled" by being in a preset; it reaches an agent via that preset→agent pairing. The user owns these pairings — do not change sync strategy on your own.

## External workspaces (`--skills-root`)

`./skills-manager-cli.exe --skills-root <dir> ...` creates an **external workspace**: it treats `<dir>` as the skills location and writes a **separate** DB under `~/.skills-manager/external/skills-<hash>/`. Only use this if you want an isolated workspace decoupled from the central repo. For normal "make Hermes load more skills" needs, the junction + `sync --tool hermes` approach is simpler and is what the built-in tool definition is designed for.

## DB layout (read-only inspection)

`~/.skills-manager/skills-manager.db` (SQLite). Useful tables:
- `skills` — managed skills (id, name, path, source_type, source_ref, presets).
- `skill_targets` — per (skill, tool) sync targets with `target_path`, `mode` (symlink), `status`.
- `projects` — project/workspace records (id, name, path, workspace_type, linked_agent_key).
- `settings` — `tool_order`, `default_scenario`, `git_backup_remote_url`, etc.

## Pitfalls

- **git-bash `cmd //c mklink /J` can fail silently / drop into a shell** — it printed the cmd banner and did nothing. Prefer `os.symlink(..., target_is_directory=True)` from Python for creating the junction.
- **`--skills-root` test creates real dirs** under `~/.skills-manager/external/`. Clean them up (`rm -rf`) after probing, or they accumulate.
- **Don't hand-edit the DB** for tool enabled/installed state — flip it via the junction (detection) and `skills sync` (deployment). Editing the DB bypasses the app's invariants.
- **GUI + CLI share one DB** — CLI changes are visible in the GUI; if the GUI looks stale, let it refresh (it re-queries on startup/focus).
- **Binaries are stripped Rust** — don't waste time `strings`-grepping for the override/custom-tool mechanism; the junction approach works without it.