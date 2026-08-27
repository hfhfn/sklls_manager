@echo off
setlocal

REM ---- editable by agent or user ----
set "PY=python"
set "URL=<URL>"
set "WORK=<WORK>"
set "SKILL=C:/Users/hfhfn/<BASE>/skills/video2markdown/scripts/video2md.py"
set "DL=C:/Users/hfhfn/<BASE>/skills/video2markdown/templates/download_douyin.py"
set "COOKIES=%WORK%\cookies.txt"

echo ============================================================
echo  video2markdown one-click: download then transcribe
echo ============================================================
echo.

where conda >nul 2>nul
if not errorlevel 1 (
    call conda activate llm_gpu >nul 2>nul
)

echo [1/3] download video ...
echo  URL: %URL%
echo.

"%PY%" "%DL%" "%URL%" "%WORK%ideo" "%COOKIES%"

rem ---- locate downloaded mp4 ----
set "MP4="
for /r "%WORK%ideo" %%F in (*.mp4) do set "MP4=%%F"
if not defined MP4 (
    echo.
    echo  !! no mp4 produced -- download failed, see log above.
    pause
    exit /b 1
)
echo.
echo  Download OK: %MP4%
echo.

echo [2/3] transcribe / OCR / describe ...
"%PY%" "%SKILL%" "%MP4%" --work "%WORK%" --depth standard --engine sensevoice

echo.
echo [done] markdown output in:
echo    %WORK%
echo.
pause
endlocal

