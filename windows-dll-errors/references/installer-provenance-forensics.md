# Worked case: `C:\jaiwcdzzydmz.exe` — "剪映安装器" that was actually 汽水音乐, from a dead third-party mirror

Second half of the Wacatac session. The missing-DLL remnant (`Bctive\`) was cleaned (see bctive-wacatac-case.md); this case is the *companion installer* found at the same minute, and how to judge it.

## Context
- 07-21 13:12: `C:\jaiwcdzzydmz.exe` (145,061,704 bytes) appeared in C:\ root — same minute as the `Bctive\` malware dir.
- User believed it was a 剪映 (Jianying/CapCut) installer. NeatDM log proved otherwise.

## Identity — signature + version resource (PowerShell garbled it, Python didn't)
```bash
powershell.exe -NoProfile -Command 'Get-AuthenticodeSignature "C:\jaiwcdzzydmz.exe" | Format-List Status,SignerCertificate'
# Status: Valid
# Subject: CN="Douyin Vision Co., Ltd."  Issuer: DigiCert Trusted G4 Code Signing RSA4096 SHA384 2021 CA1
# Valid 2023-10-17 → 2026-10-18, sha256RSA
```
PowerShell `VersionInfo.ProductName` → `???????` (GBK garble). Python UTF-16LE version-resource parse gave the truth:
```python
import re
data = open(r"C:\jaiwcdzzydmz.exe", "rb").read()
for key in ["ProductName", "LegalCopyright", "ProductVersion"]:
    k16 = key.encode("utf-16-le")
    p = data.find(k16)
    vstart = p + len(k16) + 1
    vstart = (vstart + 3) & ~3
    vend = data.find(b"\x00\x00", vstart)
    print(key, ":", data[vstart:vend].decode("utf-16-le", errors="replace"))
# ProductName: 汽水音乐   (Qishui Music — Bytedance/Douyin's music app, NOT 剪映)
# LegalCopyright: © 2024 Beijing Douyin Technology Co., Ltd
# ProductVersion: 3.1.x
```
Lesson: same parent company (Douyin) ships multiple products; filename/version-claim alone is not identity.

## Authenticode tamper check — was the signed file modified after signing?
```python
import struct
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]   # PE header offset — never scan for b"PE\0\0"
coff = e_lfanew + 4                                 # COFF header (20 bytes)
opt = coff + 20                                     # optional header
dd_off = opt + 96                                   # data directory table (16 entries × 8 bytes)
cert_rva, cert_size = struct.unpack_from("<II", data, dd_off + 4*8)   # DataDir[4] = Security
# For the security dir, cert_rva IS a file offset (not a typical RVA)
print(hex(cert_rva), cert_size, "filesize:", len(data))
# 0x8A54790, 12216, 145061704 (0x8A57748)  → cert_off + size == filesize → ZERO bytes after signature
```
If bytes exist AFTER the cert table → file was modified post-signing (Authenticode only covers [0, cert_off)). Zero-tail = genuine, unmodified binary.

## NSIS detection — the big overlay
- 5 sections (`.text/.rdata/.data/.ndata/.rsrc`), last section ends 0xD400, file is 145MB → 138MB overlay.
- Overlay starts `00000000 efbeadde 4e756c6c736f6674496e737474` = `\x00\x00\x00\x00` + `0xDEADBEEF` + `NullsoftInst` → **NSIS installer** (self-extracting; payload compressed — no readable file list inside).
- String hits in overlay: `Nullsoft`, `Uninstall`, `Douyin`, `Bytedance` (2×), and NO hits for `Bctive/falcon/security_cad` → the malicious DLL was NOT inside this signed installer; it arrived as a separate drop from the same hosting session.

## Defender per-file scan (cloud engines)
```bash
"/c/Program Files/Windows Defender/MpCmdRun.exe" -Scan -ScanType 3 -File "C:\jaiwcdzzydmz.exe"
# Scan starting... Scan finished. Scanning C:\jaiwcdzzydmz.exe found no threats.
```
Also confirmed `Get-MpThreat` / `Get-MpThreatDetection` had NO record for this file (only the falcon.dll Wacatac hit).

## Provenance — download-manager DB mining (the decisive step)
NeatDM stores history in `%APPDATA%\NeatDM\NeatDB.db`, table `downloads`:
```python
import sqlite3, datetime
con = sqlite3.connect(r"C:\Users\hfhfn\AppData\Roaming\NeatDM\NeatDB.db")
cur = con.cursor()
cur.execute("SELECT url, filename, filesize, firsttry, pageurl, pagetitle FROM downloads WHERE filename LIKE '%QISHUI%'")
for r in cur.fetchall():
    print(datetime.datetime.fromtimestamp(r[3]), r[1], r[2], r[4], r[5])
# 2026-07-21 13:12:11  QISHUIl_setup_X64639.zip  145275554
#   url:  https://qishuitasu.oss-cn-hongkong.aliyuncs.com/QISHUIl_setup_X64639.zip
#   page: https://qishuiwrtxz.com/
```
- **Timestamp correlation**: download firsttry 13:12:11 ↔ `Bctive\` mtime 13:12 ↔ installer mtime 13:12. Exact-minute match ties all three to one event.
- **Source assessment**: `qishuiwrtxz.com` is a third-party mirror (NOT official store/app-store). Now dead: site returns 400 (nginx), OSS bucket returns 404 `NoSuchBucket`. Hostile/vanished source.
- Chrome/Edge History DB (`<User Data>\Default\History`, table `downloads`, columns `target_path, tab_url, referrer, start_time[WebKit µs since 1601], danger_type`) had no record of it — the download went through NeatDM, not the browser.

## Run/install traces (none found → never completed)
- Prefetch: `dir C:\Windows\Prefetch\*JAIWC* *QISHUI* *SECURITY*` → empty (never executed, or executed before prefetch rotation).
- Uninstall registry, `AppData\Local\*qishui*` → nothing. No 汽水音乐 install.

## Verdict
- Installer FILE: genuine, unmodified, valid Douyin signature, zero AV hits → **not malware itself**.
- Installer SOURCE: hostile third-party mirror (dead now) that bundled the Wacatac drop in the same session → **don't trust the origin, don't re-download from it**.
- Disposition: no install traces + source dead → the 145MB file is useless residue; recommend deleting it.

## Reusable recipe summary
1. Python version-resource parse (UTF-16LE) for true product identity — never trust GBK-mangled PowerShell output or the filename.
2. Cert-table-at-EOF check → modified-after-signing? (tail bytes = tampered).
3. `efbeadde`+`NullsoftInst` overlay → NSIS installer; compressed payload = no file list.
4. `MpCmdRun -Scan -ScanType 3 -File` for a per-file cloud verdict.
5. Mine `NeatDB.db` (NeatDM) / browser `History` DBs for the download URL + page.
6. Correlate epoch timestamps (download ↔ dir mtime) — same-minute is the smoking gun.
7. Prefetch/uninstall/AppData sweep to decide installed-vs-abandoned.
