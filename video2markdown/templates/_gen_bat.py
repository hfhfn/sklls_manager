# -*- coding: utf-8 -*-
"""生成 run_transcribe.bat 模板：纯 ASCII + CRLF。修复 \\video 转义为垂直制表符的 bug。"""
lines = [
    "@echo off",
    "setlocal",
    "",
    "REM ---- editable by agent or user ----",
    'set "PY=python"',
    'set "URL=<URL>"',
    'set "WORK=<WORK>"',
    'set "SKILL=C:/Users/hfhfn/<BASE>/skills/video2markdown/scripts/video2md.py"',
    'set "DL=C:/Users/hfhfn/<BASE>/skills/video2markdown/templates/download_douyin.py"',
    'set "COOKIES=%WORK%\\cookies.txt"',
    "",
    "echo ============================================================",
    "echo  video2markdown one-click: download then transcribe",
    "echo ============================================================",
    "echo.",
    "",
    "where conda >nul 2>nul",
    "if not errorlevel 1 (",
    "    call conda activate llm_gpu >nul 2>nul",
    ")",
    "",
    "echo [1/3] download video ...",
    "echo  URL: %URL%",
    "echo.",
    "",
    '"%PY%" "%DL%" "%URL%" "%WORK%\\video" "%COOKIES%"',
    "",
    "rem ---- locate downloaded mp4 ----",
    'set "MP4="',
    'for /r "%WORK%\\video" %%F in (*.mp4) do set "MP4=%%F"',
    "if not defined MP4 (",
    "    echo.",
    "    echo  !! no mp4 produced -- download failed, see log above.",
    "    pause",
    "    exit /b 1",
    ")",
    "echo.",
    "echo  Download OK: %MP4%",
    "echo.",
    "",
    "echo [2/3] transcribe / OCR / describe ...",
    '"%PY%" "%SKILL%" "%MP4%" --work "%WORK%" --depth standard --engine sensevoice',
    "",
    "echo.",
    "echo [done] markdown output in:",
    "echo    %WORK%",
    "echo.",
    "pause",
    "endlocal",
    "",
]
text = "\r\n".join(lines) + "\r\n"
with open(r"C:\Users\hfhfn\AppData\Local\hermes\skills\video2markdown\templates\run_transcribe.bat",
          "w", encoding="ascii", newline="") as f:
    f.write(text)
data = open(r"C:\Users\hfhfn\AppData\Local\hermes\skills\video2markdown\templates\run_transcribe.bat",
            "rb").read()
print("run_transcribe.bat 已重写。")
print("CRLF 计数:", data.count(b"\r\n"))
print("含 0x0B 垂直制表符?", b"\x0b" in data)
print("含正确字面 WORK%\\video?", b"WORK%\\video" in data)
print("含非 ASCII?", any(b > 127 for b in data))
print("BOM?", data[:3] == b"\xef\xbb\xbf")