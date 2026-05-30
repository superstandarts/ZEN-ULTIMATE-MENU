@echo off
title ZEN ULTIMATE MENU - Requirements Installer
color 0F

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
    pause
    exit /b
)

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Install failed. Try running as administrator.
    pause
    exit /b
)

echo.
echo Installation completed.
pause
