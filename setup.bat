@echo off
echo Setting up Task CLI Manager for global access...
echo.

REM Create a bin directory in user profile if it doesn't exist
if not exist "%USERPROFILE%\bin" (
    mkdir "%USERPROFILE%\bin"
    echo Created %USERPROFILE%\bin directory
)

REM Copy the batch file to the bin directory
copy "mytasks.bat" "%USERPROFILE%\bin\mytasks.bat"
echo Copied mytasks.bat to %USERPROFILE%\bin

REM Check if user's bin directory is in PATH
echo.
echo Checking if %USERPROFILE%\bin is in your PATH...
echo %PATH% | findstr /C:"%USERPROFILE%\bin" >nul
if %errorlevel% equ 0 (
    echo ✅ %USERPROFILE%\bin is already in your PATH
    echo You can now run 'mytasks' from any terminal!
) else (
    echo ⚠️  %USERPROFILE%\bin is NOT in your PATH
    echo.
    echo To add it to your PATH, run this command in an Administrator Command Prompt:
    echo setx PATH "%PATH%;%USERPROFILE%\bin" /M
    echo.
    echo Or add it manually through System Properties ^> Environment Variables
    echo.
    echo After updating PATH, restart your terminal and run 'mytasks'
)

echo.
echo Setup complete! 
echo CSV file will be stored at: F:\Sepano-Project\تایم های کاری.csv
echo.
pause
