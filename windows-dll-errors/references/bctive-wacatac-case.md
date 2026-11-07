# Worked case: security_cad.exe → "找不到 falcon.dll" (Trojan:Win32/Wacatac.B!ml)

Full session example that produced this skill. Symptoms, root cause, and the exact commands that worked.

## Symptom
Windows error dialog at app start:
```
security_cad.exe - 系统错误
由于找不到falcon.d（falcon.dll），无法继续执行代码。重新安装程序可能会解决此问题。
```

## Root cause timeline
| Time | Event |
|---|---|
| 07-21 13:12 | `C:\Users\Public\Documents\Bctive\` created with `security_cad.exe`, `falcon.dll`, `322.txt` (empty), `unload.txt` (261KB binary/encrypted). Same minute a 145MB random-name installer `C:\jaiwcdzzydmz.exe` appeared in C:\ root. Also `C:\Users\Public\Documents\Wctive\helper.lnk` → points to security_cad.exe |
| 07-22 09:00 | **Windows Defender detected `Bctive\falcon.dll` as `Trojan:Win32/Wacatac.B!ml` (SeverityID 5) and removed it** |
| after | any launch of security_cad.exe → "missing falcon.dll" dialog |

## Key diagnostic commands that found it

1. Narrow search (full-drive `dir /s /b` and `find /c` both TIMED OUT at 30s):
   ```bash
   powershell.exe -NoProfile -Command 'Get-ChildItem -Path "C:\","D:\" -Recurse -Filter "security_cad*" -ErrorAction SilentlyContinue | Select-Object -ExpandProperty FullName'
   # → C:\Users\Public\Documents\Bctive\security_cad.exe
   ```

2. Identify the exe (was a renamed iQIYI browser component):
   ```bash
   powershell.exe -NoProfile -Command '(Get-Item "...\security_cad.exe").VersionInfo | Format-List FileDescription,ProductName,CompanyName,FileVersion,OriginalFilename'
   # OriginalFilename: QyBrowser.exe
   powershell.exe -NoProfile -Command 'Get-AuthenticodeSignature "...\security_cad.exe" | Select-Object -ExpandProperty SignerCertificate | Format-List Subject,Issuer,NotAfter'
   # CN="BEIJING QIYI CENTURY SCIENCE&TECHNOLOGY CO.,LTD." (爱奇艺), cert expired 2020
   ```
   PE strings (Python regex over raw bytes, both ASCII and UTF-16LE) revealed:
   `getFalconInstance`, `G:\chromium\src\out\Release\QyBrowser.pdb`, `\PluginConfig\falcon_subprocess\QySubProcess.log` → chromium-based browser subprocess.

3. PE import table (Python, `e_lfanew` at offset 0x3C — naive `PE\0\0` scan found wrong offset):
   First import = `falcon.dll`, plus KERNEL32/ADVAPI32/SHELL32/ole32/SHLWAPI/WS2_32.

4. **Defender history = smoking gun:**
   ```bash
   powershell.exe -NoProfile -Command 'Get-MpThreat | Select-Object ThreatName,SeverityID'
   # ThreatName : Trojan:Win32/Wacatac.B!ml   SeverityID : 5
   powershell.exe -NoProfile -Command 'Get-MpThreatDetection | Select-Object ThreatID,@{N="Resource";E={$_.Resources -join ","}},InitialDetectionTime | Format-Table -AutoSize'
   # 2147735505  file:_C:\Users\Public\Documents\Bctive\falcon.dll  2026/7/22 9:00:03
   ```

5. Startup-hook sweep came back clean (Run/RunOnce/Startup folders/schtasks/services/WMI/IFEO/AppInit/Winlogon/GPO) → remnant, not a legit program.

6. ACL revealed anti-deletion protection:
   ```bash
   powershell.exe -NoProfile -Command '(Get-Acl "...\security_cad.exe").Access | Format-Table IdentityReference,FileSystemRights,AccessControlType -AutoSize'
   # BUILTIN\Users ... Delete ... Deny   ← malware's self-protection
   # Owner: BUILTIN\Administrators
   ```
   Plain `rmdir /s /q` and `Remove-Item -Force` both failed with 拒绝访问 (access denied).

## Fix (elevated cleanup)
Non-admin terminal → write cleanup .ps1 → `Start-Process powershell -Verb RunAs` (user clicks UAC):

```powershell
# cleanup.ps1
$targets = @("C:\Users\Public\Documents\Bctive","C:\Users\Public\Documents\Wctive")
foreach ($t in $targets) {
  takeown /F $t /R /D Y 2>&1 | Out-Null
  icacls $t /grant "*S-1-5-32-544:(OI)(CI)F" /T /C 2>&1 | Out-Null   # Administrators
  icacls $t /grant "*S-1-5-32-545:(OI)(CI)F" /T /C 2>&1 | Out-Null   # Users
  icacls $t /remove:d "*S-1-5-32-545" /T /C 2>&1 | Out-Null          # strip Deny ACEs
  Remove-Item -Path $t -Recurse -Force
}
```
```bash
powershell.exe -NoProfile -Command 'Start-Process powershell -Verb RunAs -ArgumentList "-NoProfile","-ExecutionPolicy","Bypass","-File","C:\Users\hfhfn\AppData\Local\hermes\scripts\cleanup_bctive.ps1" -Wait'
```
Verify: `Test-Path` → False for all targets. Delete temp script + output file.

## Signs of a bundled-downloader event (context to look for)
- `C:\<random-letters>.exe` installer in drive root (here `jaiwcdzzydmz.exe`, 145MB, valid Douyin/Jianying signature — the bait).
- Remnant dirs with odd names (`Bctive`, `Wctive`) in `C:\Users\Public\Documents\` created at the SAME timestamp as the installer.
- Renamed/repackaged browser component (OriginalFilename mismatch) + empty/binary sidecar files (`322.txt`, `unload.txt`).
- Defender already did the hard work (quarantined the DLL); agent's job is removing the rest so the dialog stops.
