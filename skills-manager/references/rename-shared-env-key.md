# Renaming a shared credential env var (all locations)

When a key is shared across agents via the **Windows user-level env var** pattern, a
rename (e.g. `HERMES_CUSTOM_GLM_API_KEY` → `CUSTOM_GLM_API_KEY`) must touch EVERY
place the old name appears, or one agent silently keeps reading a stale name. The
name is a convention, not a standard — nothing migrates it for you.

## All the places to search & update

1. **Hermes `.env`** — `C:\Users\hfhfn\AppData\Local\hermes\.env` (the `NAME=value` definition).
2. **Hermes `config.yaml`** — `key_env:` entries (e.g. under `model:` and `providers.<name>:`) and `auxiliary.vision` if it references the key env. Edit with python text-replace (safer than `hermes config set` for nested key_env; patch may be blocked on config.yaml).
3. **Windows registry** — `HKCU\Environment`. Set the NEW name, DELETE the OLD name, then broadcast `WM_SETTINGCHANGE` (else already-running sessions keep the old var).
4. **Skill files that read the env var** — in the central dir `~/.skills-manager/skills/<skill>/` (e.g. `vision.js` `process.env.X || ...` fallback, and the skill's `SKILL.md`). Because syncs are symlinks back to the central dir, editing the central copy propagates to all synced agents automatically.
5. **The `skills-manager` skill doc itself** — keep the doc's examples in sync so future sessions don't re-introduce the old name.

## Procedure

```bash
# 1. Find every reference (do this FIRST so nothing is missed)
grep -rn OLD_NAME /c/Users/hfhfn/AppData/Local/hermes/.env \
                  /c/Users/hfhfn/AppData/Local/hermes/config.yaml \
                  /c/Users/hfhfn/.skills-manager/skills/ \
                  /c/Users/hfhfn/AppData/Local/hermes/skills/ \
                  /c/Users/hfhfn/AppData/Local/hermes/memories/
```

2. Replace in `.env`, `config.yaml`, and each skill file (python `io` read/replace/write, keep newline style).
3. Registry: `winreg.SetValueEx(NEW)` + `winreg.DeleteValue(OLD)` on `HKCU\Environment`, then `SendMessageTimeoutW(WM_SETTINGCHANGE)`.
4. Verify: `grep -rn OLD_NAME ...` → zero hits; registry has NEW and not OLD.

## Verifying the new name actually works (end-to-end)

The strongest check is to run the consuming skill in a **fresh subprocess** with ONLY
the new env var set (strip the old name from the env so a stale read can't mask a
bug), then confirm the API call authenticates. Distinguish auth failure from rate-limit:
- **401 / 403 / "invalid key"** → the env var or key is wrong (real problem).
- **429 / "访问量过大" (rate limit)** → the key validated fine; the service is just
  busy. This is NOT a config problem — retry later. (Zhipu GLM-4.6V-Flash 429s regularly.)

```python
# fresh-subprocess check pattern
env = dict(os.environ); env.pop(OLD, None); env[NEW] = value
subprocess.run(["node", vision_js, img, "描述"], capture_output=True, text=True, env=env)
```

Note: `curl` from git-bash often fails (HTTP 000) where python `urllib` succeeds —
use python for the verification call.