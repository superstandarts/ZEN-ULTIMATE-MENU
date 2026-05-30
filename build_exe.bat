@echo off
setlocal EnableExtensions EnableDelayedExpansion
title ZEN MENU - Professional Builder
color 0F

cd /d "%~dp0"

set "APP_NAME=ZEN MENU"
set "MAIN_SCRIPT=main.py"
set "ICON_PATH=assets\icons\app.ico"
set "BUILD_MODE=onefile"
set "WINDOW_MODE=windowed"
set "CLEAN_BUILD=1"

:MENU
cls
echo.
echo ============================================================
echo              ZEN MENU - BUILD CENTER
echo ============================================================
echo.
echo  App name      : %APP_NAME%
echo  Main script   : %MAIN_SCRIPT%
echo  Icon          : %ICON_PATH%
echo  Build mode    : %BUILD_MODE%
echo  Window mode   : %WINDOW_MODE%
echo  Clean build   : %CLEAN_BUILD%
echo.
echo ------------------------------------------------------------
echo  1. Build EXE now
echo  2. Change app name
echo  3. Change main script
echo  4. Change icon path
echo  5. Toggle onefile / onedir
echo  6. Toggle windowed / console
echo  7. Toggle clean build
echo  8. Install / update builder requirements
echo  9. Clean build folders only
echo  0. Exit
echo ------------------------------------------------------------
echo.
set /p "choice=Choose an option: "

if "%choice%"=="1" goto BUILD
if "%choice%"=="2" goto CHANGE_NAME
if "%choice%"=="3" goto CHANGE_SCRIPT
if "%choice%"=="4" goto CHANGE_ICON
if "%choice%"=="5" goto TOGGLE_MODE
if "%choice%"=="6" goto TOGGLE_WINDOW
if "%choice%"=="7" goto TOGGLE_CLEAN
if "%choice%"=="8" goto INSTALL_REQS
if "%choice%"=="9" goto CLEAN_ONLY
if "%choice%"=="0" exit /b 0
goto MENU

:CHANGE_NAME
echo.
set /p "APP_NAME=New app name: "
goto MENU

:CHANGE_SCRIPT
echo.
set /p "MAIN_SCRIPT=Main script path: "
goto MENU

:CHANGE_ICON
echo.
set /p "ICON_PATH=Icon path (.ico): "
goto MENU

:TOGGLE_MODE
if /I "%BUILD_MODE%"=="onefile" (
    set "BUILD_MODE=onedir"
) else (
    set "BUILD_MODE=onefile"
)
goto MENU

:TOGGLE_WINDOW
if /I "%WINDOW_MODE%"=="windowed" (
    set "WINDOW_MODE=console"
) else (
    set "WINDOW_MODE=windowed"
)
goto MENU

:TOGGLE_CLEAN
if "%CLEAN_BUILD%"=="1" (
    set "CLEAN_BUILD=0"
) else (
    set "CLEAN_BUILD=1"
)
goto MENU

:INSTALL_REQS
cls
echo.
echo ============================================================
echo Installing builder requirements...
echo ============================================================
echo.
python -m pip install --upgrade pip setuptools wheel
python -m pip install pyinstaller
if exist requirements.txt (
    python -m pip install -r requirements.txt
)
echo.
pause
goto MENU

:CLEAN_ONLY
call :CLEAN_FOLDERS
echo.
echo Clean finished.
pause
goto MENU

:BUILD
cls
echo.
echo ============================================================
echo Building %APP_NAME%
echo ============================================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python was not found in PATH.
    echo Install Python and enable "Add Python to PATH".
    pause
    goto MENU
)

if not exist "%MAIN_SCRIPT%" (
    echo [ERROR] Main script not found: %MAIN_SCRIPT%
    pause
    goto MENU
)

if "%CLEAN_BUILD%"=="1" (
    call :CLEAN_FOLDERS
)

python -m pip show pyinstaller >nul 2>nul
if errorlevel 1 (
    echo [INFO] PyInstaller not found. Installing...
    python -m pip install pyinstaller
)

set "PYI_ARGS=--noconfirm"

if "%CLEAN_BUILD%"=="1" set "PYI_ARGS=%PYI_ARGS% --clean"

if /I "%BUILD_MODE%"=="onefile" (
    set "PYI_ARGS=%PYI_ARGS% --onefile"
) else (
    set "PYI_ARGS=%PYI_ARGS% --onedir"
)

if /I "%WINDOW_MODE%"=="windowed" (
    set "PYI_ARGS=%PYI_ARGS% --windowed"
) else (
    set "PYI_ARGS=%PYI_ARGS% --console"
)

if exist "%ICON_PATH%" (
    set "PYI_ARGS=%PYI_ARGS% --icon "%ICON_PATH%""
    echo [INFO] Using icon: %ICON_PATH%
) else (
    echo [WARNING] Icon not found: %ICON_PATH%
    echo [WARNING] Building without icon.
)

echo.
echo [INFO] PyInstaller args:
echo %PYI_ARGS%
echo.

python -m PyInstaller %PYI_ARGS% --name "%APP_NAME%" "%MAIN_SCRIPT%"

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed.
    pause
    goto MENU
)

echo.
echo [INFO] Copying external files to dist...

if not exist "dist" mkdir dist

if exist "config.json" copy /Y "config.json" "dist\config.json" >nul
if exist "README.txt" copy /Y "README.txt" "dist\README.txt" >nul
if exist "README.md" copy /Y "README.md" "dist\README.md" >nul
if exist "CHANGELOG.md" copy /Y "CHANGELOG.md" "dist\CHANGELOG.md" >nul

if exist "assets" (
    xcopy /E /I /Y "assets" "dist\assets" >nul
)

if exist "plugins" (
    xcopy /E /I /Y "plugins" "dist\plugins" >nul
)

echo.
echo ============================================================
echo Build finished successfully.
echo Output folder: dist
echo.
echo Important:
echo Keep config.json and assets next to the EXE.
echo ============================================================
echo.
pause
goto MENU

:CLEAN_FOLDERS
echo [INFO] Cleaning build artifacts...
if exist build rmdir /S /Q build
if exist dist rmdir /S /Q dist
del /Q "*.spec" >nul 2>nul
exit /b 0
