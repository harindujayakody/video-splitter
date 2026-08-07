@echo off
setlocal EnableExtensions
title Split Video Pro - Setup and Launcher
cd /d "%~dp0"

echo ============================================================
echo                    Split Video Pro
echo                  Setup and Launcher
echo ============================================================
echo Author : Harindu Jayakody
echo Website: Infiax.com
echo.

set "PYTHON_CMD="
where py >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON_CMD=py -3"
) else (
    where python >nul 2>nul
    if %errorlevel%==0 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
    echo [ERROR] Python 3 was not found.
    echo Install Python 3.9 or newer from https://www.python.org/downloads/
    echo Enable "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [OK] Python found.
%PYTHON_CMD% --version
echo.

%PYTHON_CMD% -m pip --version >nul 2>nul
if errorlevel 1 (
    echo [INFO] pip is missing. Attempting installation...
    %PYTHON_CMD% -m ensurepip --upgrade
    if errorlevel 1 (
        echo [ERROR] Could not install pip automatically.
        pause
        exit /b 1
    )
)

echo [OK] pip found.
echo.

if exist "%~dp0requirements.txt" (
    echo [INFO] Checking/installing Python requirements...
    %PYTHON_CMD% -m pip install --disable-pip-version-check -r "%~dp0requirements.txt"
    if errorlevel 1 (
        echo [ERROR] Python dependency installation failed.
        pause
        exit /b 1
    )
    echo [OK] Python requirements are ready.
) else (
    echo [ERROR] requirements.txt was not found.
    pause
    exit /b 1
)
echo.

where ffmpeg >nul 2>nul
set "HAS_FFMPEG=%errorlevel%"
where ffprobe >nul 2>nul
set "HAS_FFPROBE=%errorlevel%"
if "%HAS_FFMPEG%"=="0" if "%HAS_FFPROBE%"=="0" goto ffmpeg_ready

echo [WARN] FFmpeg or FFprobe is missing.
echo [INFO] Checking for Windows Package Manager ^(winget^)...
where winget >nul 2>nul
if errorlevel 1 (
    echo [ERROR] winget is unavailable, so FFmpeg cannot be installed automatically.
    echo Install FFmpeg manually from https://ffmpeg.org/download.html
    echo.
    pause
    exit /b 1
)

echo [INFO] Attempting FFmpeg installation using winget...
winget install --id Gyan.FFmpeg -e --accept-package-agreements --accept-source-agreements
if errorlevel 1 (
    echo [ERROR] FFmpeg automatic installation failed.
    echo Install it manually from https://ffmpeg.org/download.html
    pause
    exit /b 1
)

echo.
echo [INFO] FFmpeg installation command completed.
where ffmpeg >nul 2>nul
if errorlevel 1 (
    echo [WARN] FFmpeg is not visible in this terminal yet.
    echo Close this window and run "Split Video Pro.bat" again so PATH refreshes.
    pause
    exit /b 0
)

:ffmpeg_ready
echo [OK] FFmpeg found.
ffmpeg -version 2>nul | findstr /b /c:"ffmpeg version"
echo.

if not exist "%~dp0input" mkdir "%~dp0input"
if not exist "%~dp0output" mkdir "%~dp0output"

echo [INFO] Starting Split Video Pro...
echo.
%PYTHON_CMD% "%~dp0split_video_pro.py"

echo.
echo Split Video Pro has closed.
pause
endlocal
