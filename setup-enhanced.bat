@echo off
echo ========================================
echo Task CLI Manager - Setup Script
echo ========================================
echo.

REM Get the current directory
set CURRENT_DIR=%cd%

echo Installing Task CLI Manager globally...
echo.

REM Check if user bin directory exists, if not create it
if not exist "%USERPROFILE%\bin" (
    mkdir "%USERPROFILE%\bin"
    echo Created %USERPROFILE%\bin directory
)

REM Copy batch file for Command Prompt
copy "%CURRENT_DIR%\mytasks.bat" "%USERPROFILE%\bin\" >nul
if %errorlevel% equ 0 (
    echo ✓ Installed mytasks.bat for Command Prompt
) else (
    echo ✗ Failed to install mytasks.bat
)

REM Copy PowerShell script
copy "%CURRENT_DIR%\mytasks.ps1" "%USERPROFILE%\bin\" >nul
if %errorlevel% equ 0 (
    echo ✓ Installed mytasks.ps1 for PowerShell
) else (
    echo ✗ Failed to install mytasks.ps1
)

echo.
echo Checking PATH configuration...

REM Check if %USERPROFILE%\bin is in PATH
echo %PATH% | find /i "%USERPROFILE%\bin" >nul
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  %USERPROFILE%\bin is not in your PATH
    echo.
    echo To complete the setup, add %USERPROFILE%\bin to your PATH:
    echo.
    echo Method 1 - Automatic (requires admin):
    echo   Run: setx PATH "%PATH%;%USERPROFILE%\bin" /M
    echo.
    echo Method 2 - Manual:
    echo   1. Open System Properties ^> Environment Variables
    echo   2. Edit the PATH variable
    echo   3. Add: %USERPROFILE%\bin
    echo.
    echo Method 3 - PowerShell Profile (PowerShell only):
    echo   Run these commands in PowerShell as Administrator:
    echo   Set-ExecutionPolicy RemoteSigned -Force
    echo   Add-Content $PROFILE 'Set-Alias mytasks "%USERPROFILE%\bin\mytasks.ps1"'
    echo.
) else (
    echo ✓ %USERPROFILE%\bin is already in PATH
)

echo.
echo Setting PowerShell execution policy for scripts...
powershell -Command "Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force" 2>nul
if %errorlevel% equ 0 (
    echo ✓ PowerShell execution policy set to RemoteSigned
) else (
    echo ⚠️  Could not set PowerShell execution policy automatically
    echo   You may need to run: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Usage:
echo   Command Prompt: mytasks
echo   PowerShell:     mytasks   or   .\mytasks.ps1
echo.
echo If 'mytasks' doesn't work, restart your terminal after updating PATH
echo CSV file location: F:\Sepano-Project\تایم های کاری.csv
echo.
pause
