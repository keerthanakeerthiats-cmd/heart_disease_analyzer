@echo off
setlocal enabledelayedexpansion

REM Automated ngrok Setup and Launch Script

echo =====================================
echo ngrok Setup and Tunnel Launcher
echo =====================================
echo.
echo This script will help you create a public URL for your Flask app.
echo.

REM Check if ngrok exists
if not exist "ngrok\ngrok.exe" (
    echo ERROR: ngrok not found!
    echo Please run this first in PowerShell:
    echo   Invoke-WebRequest -Uri "https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip" -OutFile ngrok.zip
    echo   Expand-Archive -Path ngrok.zip -DestinationPath .\ngrok -Force
    echo.
    pause
    exit /b 1
)

REM Ask for authtoken
set /p authtoken="Enter your ngrok authtoken: "

if "!authtoken!"=="" (
    echo ERROR: No authtoken provided!
    pause
    exit /b 1
)

echo.
echo Installing authtoken...
ngrok\ngrok.exe authtoken !authtoken!

if %errorlevel% neq 0 (
    echo ERROR: Failed to install authtoken. Check your token and try again.
    pause
    exit /b 1
)

echo.
echo =====================================
echo Starting ngrok tunnel on port 5001...
echo =====================================
echo.
echo Your public URL will appear below in a few seconds.
echo Once you see "Forwarding", you can share that URL with others!
echo.
echo Press Ctrl+C to stop the tunnel.
echo.

ngrok\ngrok.exe http 5001

echo.
echo Tunnel stopped. Run this script again to start a new tunnel.
pause
