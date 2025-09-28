# PowerShell Setup Script for Task CLI Manager
# Run this as Administrator in PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Task CLI Manager - PowerShell Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get current directory
$currentDir = Get-Location

# Create user bin directory if it doesn't exist
$userBin = "$env:USERPROFILE\bin"
if (!(Test-Path $userBin)) {
    New-Item -ItemType Directory -Path $userBin -Force | Out-Null
    Write-Host "✓ Created $userBin directory" -ForegroundColor Green
}

# Copy files
try {
    Copy-Item "$currentDir\mytasks.bat" "$userBin\" -Force
    Write-Host "✓ Installed mytasks.bat for Command Prompt" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to install mytasks.bat" -ForegroundColor Red
}

try {
    Copy-Item "$currentDir\mytasks.ps1" "$userBin\" -Force
    Write-Host "✓ Installed mytasks.ps1 for PowerShell" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to install mytasks.ps1" -ForegroundColor Red
}

Write-Host ""
Write-Host "Setting PowerShell execution policy..." -ForegroundColor Yellow

try {
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Host "✓ PowerShell execution policy set to RemoteSigned" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not set PowerShell execution policy" -ForegroundColor Yellow
    Write-Host "   You may need to run: Set-ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Checking PATH configuration..." -ForegroundColor Yellow

# Check if user bin is in PATH
$pathEnv = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($pathEnv -notlike "*$userBin*") {
    Write-Host ""
    Write-Host "⚠️  $userBin is not in your PATH" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Adding to PATH..." -ForegroundColor Yellow
    
    try {
        $newPath = $pathEnv + ";$userBin"
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
        Write-Host "✓ Added $userBin to PATH" -ForegroundColor Green
        Write-Host "   Please restart your terminal for changes to take effect" -ForegroundColor Cyan
    } catch {
        Write-Host "✗ Failed to add to PATH automatically" -ForegroundColor Red
        Write-Host "Please add manually: $userBin" -ForegroundColor Yellow
    }
} else {
    Write-Host "✓ $userBin is already in PATH" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Usage:" -ForegroundColor White
Write-Host "  Command Prompt: mytasks" -ForegroundColor Gray
Write-Host "  PowerShell:     mytasks" -ForegroundColor Gray
Write-Host ""
Write-Host "If 'mytasks' doesn't work, restart your terminal" -ForegroundColor Yellow
Write-Host "CSV file location: F:\Sepano-Project\تایم های کاری.csv" -ForegroundColor Gray
Write-Host ""

Read-Host "Press Enter to continue"
