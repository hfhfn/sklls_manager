---
name: windows-dll-errors
description: Fix Windows missing-DLL app-start errors; find root cause.
---

# Windows "Missing DLL / 无法继续执行代码" Troubleshooting

Use when a Windows error dialog appears like:
- `xxx.exe - 系统错误: 由于找不到 falcon.dll，无法继续执行代码。重新安装程序可能会解决此问题。`
- `The code execution cannot proceed because X.dll was not found.`
- `0xc000007b` or other app-start failures mentioning a DLL.

**Key insight: if an AV/Defender is present, the #1 hidden cause is that Defender QUARANTINED/DELETED the DLL as malware.** The dialog is a *symptom*; the exe that depends on the DLL may itself be a malware remnant that got partially cleaned. Do NOT "restore" the DLL — remove the dependent remnant instead.

## Case B: SILENT crash at startup (0xC0000005), no output — stale VC++ runtime

Distinct from the missing-DLL dialog above: the exe starts and dies instantly, printing **nothing** — not even `--help`/`--version`. On a launcher script this masquerades as "program broken / version too old" because the `--help` probe returns empty. Root cause is usually an **incompatibly OLD Microsoft VC++ runtime** (`msvcp140.dll`/`vcruntime140.dll`) sitting in `C:\Windows\System32`, not a missing DLL.

**Decisive diagnostics (do these FIRST — they short-circuit a long rabbit-hole):**

1. **Get the REAL NTSTATUS exit code via PowerShell, not bash.** bash/MSYS maps any Windows crash to `Segmentation fault` + exit `139`, which is useless. Use:
   ```bash
   powershell -NoProfile -Command "\$p=Start-Process -FilePath (Join-Path (Get-Location) 'app.exe') -ArgumentList '--help' -NoNewWindow -Wait -PassThru -RedirectStandardError e.txt -RedirectStandardOutput o.txt; Write-Host ('exit 0x{0:X8}' -f (\$p.ExitCode -band 0xFFFFFFFF))"
   ```
   `0xC0000005` = ACCESS_VIOLATION (crashed in CRT/loader init before printing). `0xC0000135` = DLL_NOT_FOUND (a genuinely missing DLL — different path).

2. **Check the Windows Application event log — it names the failing module AND its version:**
   ```bash
   powershell -NoProfile -Command "Get-WinEvent -FilterHashtable @{LogName='Application'; Id=1000} -MaxEvents 5 | ForEach-Object { \$_.TimeCreated; \$_.Properties | ForEach-Object { \$_.Value } }"
   ```
   The Properties sequence is: exe name, version, …, **faulting module name**, faulting module version, …, exception code, faulting offset. A `MSVCP140.dll` with version `14.0.24xxx` (2016-era) faulting a 2024+ binary = runtime mismatch confirmed.

3. **Compare the ACTUAL System32 runtime version vs what the registry claims is installed:**
   ```bash
   powershell -NoProfile -Command "(Get-Item 'C:\Windows\System32\msvcp140.dll').VersionInfo.FileVersion"
   powershell -NoProfile -Command "(Get-Item 'C:\Windows\System32\vcruntime140.dll').VersionInfo.FileVersion"
   reg query "HKLM\\SOFTWARE\\Microsoft\\VisualStudio\\14.0\\VC\\Runtimes\\x64"   # Installed version
   ```
   Red flag: registry says `14.44`/`14.51` (current) but System32 holds `14.0.24215` (2016) — an old runtime shadowing the newer install. That is the signature of this bug.

4. **Fix — reinstall the redist with winget (replaces the System32 runtime):**
   ```bash
   winget install --id Microsoft.VCRedist.2015+.x64 --silent --accept-package-agreements --accept-source-agreements
   ```
   Re-check the System32 version, then re-run the exe. Optionally test a CPU-only build first to prove the crash is runtime-wide and not GPU/CUDA-specific.

**Pitfalls for this case:**
- Do NOT trust bash `Segmentation fault` / exit `139` — it's the MSYS wrapper, not the real error. Always read the PowerShell `-PassThru .ExitCode`.
- Do NOT conclude "the download is corrupted" before checking integrity — files can be byte-identical to the official release (compare sizes/hashes) and still crash purely from the local runtime. The user may be on the genuinely latest version; the crash is environmental.
- A launcher's "version too old" message from a feature probe is a *symptom of the empty `--help` output*, not the truth. Don't chase version upgrades.
- Event-log LocalDumps (HKCU Key or both) often produce no dump on this crash mode; the Application/Id=1000 event is the reliable signal — don't sink time into enabling dump collection.

## Workflow

1. **Locate the exe** — full-drive `dir /s /b` and `find /` time out (30s+). Narrow first:
   ```bash
   # Check likely drop spots: Public\Documents, ProgramData, C:\ root, Downloads, D:\software
   powershell.exe -NoProfile -Command 'Get-ChildItem -Path "C:\Users\Public","C:\ProgramData","C:\" -Recurse -Filter "security_cad*" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName'
   ```
   (malware bundles love `C:\Users\Public\Documents\<weirdname>\` — also see `C:\<random>.exe` in root)

2. **Identify what the exe actually is** (renamed files are a malware tell):
   ```bash
   powershell.exe -NoProfile -Command '(Get-Item "PATH").VersionInfo | Format-List FileDescription,ProductName,CompanyName,FileVersion,OriginalFilename'
   powershell.exe -NoProfile -Command 'Get-AuthenticodeSignature "PATH" | Format-List Status,SignerCertificate'
   ```
   `OriginalFilename` revealing a different name (e.g. `QyBrowser.exe`) + PDB path in strings (`G:\chromium\src\...`) = repackaged component.

3. **Parse PE import table** (Python) to confirm which DLLs it needs — use `e_lfanew` at offset **0x3C**, never scan for `PE\0\0`:
   ```python
   import struct
   data = open(path,'rb').read()
   pe = struct.unpack_from('<I', data, 0x3C)[0]
   # then parse import directory RVA at opt+104 (PE32) / opt+112 (PE32+), convert RVA->offset via section headers
   ```
   The missing DLL is typically the FIRST import.

4. **CHECK DEFENDER HISTORY — the decisive step:**
   ```bash
   powershell.exe -NoProfile -Command 'Get-MpThreat | Select-Object ThreatName,SeverityID'
   powershell.exe -NoProfile -Command 'Get-MpThreatDetection | Select-Object ThreatID,@{N="Resource";E={$_.Resources -join ","}},InitialDetectionTime | Format-Table -AutoSize'
   ```
   If you see the DLL listed with a Trojan name (e.g. `Trojan:Win32/Wacatac.B!ml`, severity 5) — root cause confirmed.

5. **Confirm nothing legitimately auto-launches it** (clean hooks = remnant, safe to delete):
   - Registry Run/RunOnce: `HKLM\...\CurrentVersion\Run`, `RunOnce`, `WOW6432Node` variants, `HKCU` variants
   - Startup folders: `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp\` and `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`
   - `schtasks /query`, services (`sc query type= service state= all`), WMI subscriptions (`Get-CimInstance -Namespace root\subscription -ClassName __EventConsumer`)
   - IFEO (`...\Image File Execution Options`), AppInit_DLLs, Winlogon `Userinit`/`Shell`, Group Policy script dirs
   - Find `.lnk` references: `powershell.exe -NoProfile -Command '$sh=New-Object -ComObject WScript.Shell; $sh.CreateShortcut("PATH").TargetPath'`

6. **Check ACL for anti-deletion protection** (malware sets `Deny Delete` for Users, owner=Administrators):
   ```bash
   powershell.exe -NoProfile -Command '(Get-Acl "PATH").Access | Format-Table IdentityReference,FileSystemRights,AccessControlType -AutoSize'
   ```
   A `BUILTIN\Users ... Delete ... Deny` ACE means a plain delete will fail with 拒绝访问/access denied.

7. **Elevated cleanup** — write a `.ps1` file, launch via UAC (user must click the prompt):
   ```powershell
   # cleanup.ps1
   takeown /F $t /R /D Y | Out-Null
   icacls $t /grant "*S-1-5-32-544:(OI)(CI)F" /T /C | Out-Null   # Administrators
   icacls $t /grant "*S-1-5-32-545:(OI)(CI)F" /T /C | Out-Null   # Users
   icacls $t /remove:d "*S-1-5-32-545" /T /C | Out-Null          # strip Deny ACEs
   Remove-Item -Path $t -Recurse -Force
   ```
   ```bash
   powershell.exe -NoProfile -Command 'Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile","-ExecutionPolicy","Bypass","-File","C:\path\cleanup.ps1" -Wait'
   ```
8. **Verify**: `Test-Path` each target returns False; delete the temp script.

## Second file in the bundle: installer / provenance forensics

When a remnant dir appears at the SAME MINUTE as a large random-name installer in `C:\` root (bundled-downloader event), investigate the installer too — but remember the distinction: **the signed installer file can be 100% legitimate while the third-party source that served it is what dropped the malware.** Verdict = "file OK, source hostile", not "file is malware".

1. **Read the REAL product identity** (PowerShell's GBK-mangled ProductName is unreliable; parse the version resource in Python — keys like `ProductName`/`LegalCopyright` are stored as UTF-16LE directly in the file):
   ```python
   k16 = b"ProductName".decode().encode("utf-16-le")
   p = data.find(k16); vstart = p + len(k16) + 1; vstart = (vstart + 3) & ~3
   val = data[vstart:data.find(b"\x00\x00", vstart)].decode("utf-16-le")
   ```
   (Here: `jaiwcdzzydmz.exe` claimed 剪映 but was actually **汽水音乐** — signed by the same parent company, so the filename claim and the signature alone are not enough.)

2. **Authenticode tamper check — is there data AFTER the certificate table?** A post-signing append invalidates the "genuine file" story. The Security data directory (`DataDir[4]`, at `opt+96+4*8`) holds cert-table file offset + size; if `cert_off + cert_size < filesize`, the file was modified after signing:
   ```python
   cert_rva, cert_size = struct.unpack_from("<II", data, dd_off + 4*8)  # dd_off = opt + 96
   # cert_rva IS a file offset for the security dir. cert_off+size == filesize → unmodified.
   ```
   In this case the cert table sat at EOF with zero bytes after → **genuine, unmodified** Douyin-signed file.

3. **NSIS installer detection** — stub-only PE with a huge overlay is a self-extracting installer; overlay starting `efbeadde` (LE 0xDEADBEEF) + `NullsoftInst` = NSIS. `Nullsoft`/`Uninstall`/`nsi` string hits in the overlay confirm. NSIS payload is compressed — do NOT expect readable file lists.

4. **Defender on-demand per-file scan** (cloud engines; don't trust local-only reading):
   ```bash
   "/c/Program Files/Windows Defender/MpCmdRun.exe" -Scan -ScanType 3 -File "C:\jaiwcdzzydmz.exe"
   # → "Scanning ... found no threats."
   ```

5. **Provenance: mine the download-manager + browser DBs** — this is where the hostile source is exposed:
   ```bash
   # NeatDM: %APPDATA%\NeatDM\NeatDB.db, table downloads (url, filename, firsttry[epoch], pageurl, pagetitle, folderpath)
   # Chrome/Edge: "<User Data>\Default\History", table downloads (target_path, tab_url, referrer, start_time[WebKit µs], danger_type)
   ```
   Copy the DB to temp first (live DB is locked), open with sqlite3. Found: `QISHUIl_setup_X64639.zip` from `https://qishuiwrtxz.com/` (now dead, 400/404) hosted on an Aliyun HK OSS bucket — third-party mirror, not an official store/domain.
6. **Correlate timestamps**: download `firsttry` epoch ↔ remnant-dir mtime. Exact-minute match (13:12:11 vs 13:12) is the smoking gun tying the installer to the malware drop.
7. **Check for run/install traces**: Prefetch (`dir C:\Windows\Prefetch\*NAME*`), uninstall registry, AppData product dirs. No traces + dead source URL → installer never completed / already cleaned → recommend deleting the leftover 145MB file.

## Pitfalls

- **bash eats PowerShell `$_`**: wrap the whole `-Command` in single quotes or `$_` gets expanded to `/c/Users/<user>.Name` garbage.
- **GBK encoding**: Chinese output arrives as 乱码 in git-bash. Still readable enough (lengths, ASCII fields); use PowerShell's Format-Table to keep structure.
- **Full-drive scans time out** (both `find /c` and `cmd /c dir /s`). Always narrow to suspect dirs first.
- **`Get-MpThreatDetection` Resources is an array** — join it or you see only `file:_...`.
- **Suspicious residue**: `322.txt`/`unload.txt` binary files, random-name installers in `C:\` root created at the SAME minute as the remnant dir = bundled-downloader event; check for a second installer + its signature.
- Defender deletion means the "reinstall the program" advice in the dialog is wrong — the DLL was malware, not a broken install.
- **ProductName via PowerShell `.VersionInfo` garbles on Chinese binaries** (GBK↔console mismatch yields `??????`). Parse the UTF-16LE version resource in Python instead — the filename/signature claim can be wrong (剪映 vs 汽水音乐 are different products, same parent company).
- **Signature validity ≠ file origin trust**: a valid, unmodified, correctly-signed installer can still be served by a hostile third-party mirror that bundled the malware in the same drop. Check download provenance before clearing the installer as harmless.

## Support files
- `references/bctive-wacatac-case.md` — full worked example: timeline, exact commands, elevated cleanup script that fixed it.
- `references/installer-provenance-forensics.md` — worked case: NSIS/PE overlay analysis, authenticode tamper check, NeatDM/Chrome download-DB mining, Defender per-file scan, timestamp correlation.
