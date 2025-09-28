@echo off
REM Cross-platform installer script for Windows

echo 🚀 Installing CLI Task Manager...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ from https://python.org
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Found Python %PYTHON_VERSION%

REM Create installation directory
set "INSTALL_DIR=%USERPROFILE%\.local\share\cli-task-manager"
set "BIN_DIR=%USERPROFILE%\.local\bin"

if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)
if not exist "%BIN_DIR%" (
    mkdir "%BIN_DIR%"
)

echo ✓ Created installation directory: %INSTALL_DIR%

REM Download and install
echo 📥 Downloading CLI Task Manager...
cd /d "%INSTALL_DIR%"

REM Check if git is available
git --version >nul 2>&1
if %errorlevel% equ 0 (
    REM Use git if available
    if exist ".git" (
        git pull
    ) else (
        git clone https://github.com/yourusername/cli-task-manager.git .
    )
) else (
    echo ⚠️  Git not found. Please download the source code manually.
    echo 1. Go to: https://github.com/yourusername/cli-task-manager
    echo 2. Download as ZIP
    echo 3. Extract to: %INSTALL_DIR%
    echo 4. Run this installer again
    pause
    exit /b 1
)

REM Create virtual environment
echo 🐍 Setting up Python environment...
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ✓ Installed Python dependencies

REM Create executable batch script
set "SCRIPT_PATH=%BIN_DIR%\mytasks.bat"

(
echo @echo off
echo REM CLI Task Manager executable script
echo cd /d "%INSTALL_DIR%"
echo call venv\Scripts\activate.bat
echo python main.py %%*
) > "%SCRIPT_PATH%"

echo ✓ Created executable: %SCRIPT_PATH%

REM Update PATH
echo ⚠️  Adding %BIN_DIR% to PATH
setx PATH "%PATH%;%BIN_DIR%" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Added to PATH
) else (
    echo ⚠️  Could not automatically add to PATH
    echo Please add manually: %BIN_DIR%
)

REM Test installation
echo 🧪 Testing installation...
if exist "%SCRIPT_PATH%" (
    echo ✓ Installation successful!
    echo.
    echo 🚀 You can now run: mytasks
    echo.
    echo ⚠️  Please restart your terminal for PATH changes to take effect
) else (
    echo ❌ Installation failed
    pause
    exit /b 1
)

echo.
echo ===============================================
echo ✅ Installation Complete!
echo ===============================================
echo.
echo Run "mytasks" to start the application
echo.
pause
