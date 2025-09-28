# PowerShell installer script for Windows
# Can be run directly or via install.bat

param(
    [switch]$Dev,
    [string]$InstallPath = "$env:USERPROFILE\.local\share\cli-task-manager"
)

# Set colors
$Host.UI.RawUI.ForegroundColor = "White"

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    $oldColor = $Host.UI.RawUI.ForegroundColor
    $Host.UI.RawUI.ForegroundColor = $Color
    Write-Host $Message
    $Host.UI.RawUI.ForegroundColor = $oldColor
}

Write-ColorOutput "🚀 CLI Task Manager Installer" "Cyan"
Write-ColorOutput "======================================" "Cyan"
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>$null
    Write-ColorOutput "✓ Found: $pythonVersion" "Green"
} catch {
    Write-ColorOutput "❌ Python not found. Please install Python 3.8+" "Red"
    Write-ColorOutput "Download from: https://python.org" "Yellow"
    Read-Host "Press Enter to exit"
    exit 1
}

# Create installation directories
$binDir = "$env:USERPROFILE\.local\bin"
New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
New-Item -ItemType Directory -Path $binDir -Force | Out-Null

Write-ColorOutput "✓ Created installation directory: $InstallPath" "Green"

# Download and install
Write-ColorOutput "📥 Downloading CLI Task Manager..." "Blue"

Set-Location $InstallPath

# Check if git is available
try {
    git --version | Out-Null
    if (Test-Path ".git") {
        git pull
    } else {
        git clone https://github.com/yourusername/cli-task-manager.git .
    }
} catch {
    Write-ColorOutput "⚠️  Git not found. Please download manually:" "Yellow"
    Write-ColorOutput "1. Go to: https://github.com/yourusername/cli-task-manager" "White"
    Write-ColorOutput "2. Download as ZIP" "White"
    Write-ColorOutput "3. Extract to: $InstallPath" "White"
    Read-Host "Press Enter after extracting files, then run installer again"
    exit 1
}

# Create virtual environment
Write-ColorOutput "🐍 Setting up Python environment..." "Blue"
python -m venv venv
& "venv\Scripts\Activate.ps1"

# Install dependencies
python -m pip install --upgrade pip
if ($Dev) {
    pip install -r requirements-dev.txt
} else {
    pip install -r requirements.txt
}

Write-ColorOutput "✓ Installed Python dependencies" "Green"

# Create executable scripts
$batScript = "$binDir\mytasks.bat"
$ps1Script = "$binDir\mytasks.ps1"

# Create batch script for Command Prompt
@"
@echo off
REM CLI Task Manager executable script
cd /d "$InstallPath"
call venv\Scripts\activate.bat
python main.py %*
"@ | Out-File -FilePath $batScript -Encoding ASCII

# Create PowerShell script
@"
# CLI Task Manager PowerShell script
Set-Location "$InstallPath"
& "venv\Scripts\Activate.ps1"
& python main.py @args
"@ | Out-File -FilePath $ps1Script -Encoding UTF8

Write-ColorOutput "✓ Created executables in: $binDir" "Green"

# Update PATH
Write-ColorOutput "⚠️  Adding $binDir to PATH..." "Yellow"

$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($currentPath -notlike "*$binDir*") {
    try {
        $newPath = "$currentPath;$binDir"
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
        Write-ColorOutput "✓ Added to PATH" "Green"
    } catch {
        Write-ColorOutput "⚠️  Could not automatically add to PATH" "Yellow"
        Write-ColorOutput "Please add manually: $binDir" "Yellow"
    }
} else {
    Write-ColorOutput "✓ Already in PATH" "Green"
}

# Set execution policy for PowerShell scripts
try {
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-ColorOutput "✓ Set PowerShell execution policy" "Green"
} catch {
    Write-ColorOutput "⚠️  Could not set execution policy" "Yellow"
}

# Test installation
Write-ColorOutput "🧪 Testing installation..." "Blue"

if ((Test-Path $batScript) -and (Test-Path $ps1Script)) {
    Write-ColorOutput "✓ Installation successful!" "Green"
    Write-Host ""
    Write-ColorOutput "🚀 You can now run: mytasks" "Cyan"
    Write-Host ""
    Write-ColorOutput "⚠️  Please restart your terminal for PATH changes to take effect" "Yellow"
} else {
    Write-ColorOutput "❌ Installation failed" "Red"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-ColorOutput "======================================" "Cyan"
Write-ColorOutput "✅ Installation Complete!" "Green"
Write-ColorOutput "======================================" "Cyan"
Write-Host ""
Write-ColorOutput "Usage:" "White"
Write-ColorOutput "  Command Prompt: mytasks" "Gray"
Write-ColorOutput "  PowerShell:     mytasks" "Gray"
Write-Host ""

if ($Dev) {
    Write-ColorOutput "Development mode enabled!" "Yellow"
    Write-ColorOutput "You can now contribute to the project." "White"
}

Read-Host "Press Enter to exit"
