@echo off
title ZEN ULTIMATE MENU - Requirements Installer
color 0C

cd /d "%~dp0"

echo.
echo ==========================================
echo        ZEN ULTIMATE MENU REQUIREMENTS
echo ==========================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python was not found in PATH.
    echo Install Python and check "Add Python to PATH".
    echo.
    pause
    exit /b
)

if not exist "requirements.txt" (
    echo [ERROR] requirements.txt was not found in this folder.
    echo.
    pause
    exit /b
)

echo [INFO] Python found:
python --version
echo.

echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [INFO] Installing requirements...
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Install failed.
    echo Try running as administrator.
    pause
    exit /b
)

echo.
echo ==========================================
echo        INSTALLATION COMPLETED
echo ==========================================
echo.
pause
