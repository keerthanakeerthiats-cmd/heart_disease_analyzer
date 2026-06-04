@echo off
echo ================================================================
echo Heart Disease Analyzer - Diagnostic Tool
echo ================================================================
echo.
echo This will check what's preventing your website from opening.
echo.
pause

echo.
echo [CHECK 1] Python Installation
echo ================================================================
python --version
if errorlevel 1 (
    echo.
    echo ✗ PROBLEM FOUND: Python is NOT installed or NOT in PATH
    echo.
    echo SOLUTION:
    echo   1. Download Python from: https://www.python.org/downloads/
    echo   2. During installation, CHECK "Add Python to PATH"
    echo   3. Restart computer
    echo   4. Try again
    echo.
    pause
    exit /b 1
) else (
    echo ✓ Python is installed
)

echo.
echo [CHECK 2] Project Location
echo ================================================================
cd /d "%~dp0"
echo Current directory: %CD%
if not exist "app.py" (
    echo.
    echo ✗ PROBLEM FOUND: app.py not found in current directory
    echo.
    echo SOLUTION:
    echo   Make sure you're running this from the project folder:
    echo   C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff
    echo.
    pause
    exit /b 1
) else (
    echo ✓ Found app.py
)

echo.
echo [CHECK 3] Required Files
echo ================================================================
if exist "templates\index.html" (
    echo ✓ Found templates\index.html
) else (
    echo ✗ Missing templates\index.html
)

if exist "requirements.txt" (
    echo ✓ Found requirements.txt
) else (
    echo ✗ Missing requirements.txt
)

echo.
echo [CHECK 4] Python Dependencies
echo ================================================================
echo Checking Flask...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ✗ Flask not installed
    echo.
    echo Installing Flask...
    pip install flask flask-cors
) else (
    echo ✓ Flask is installed
)

echo.
echo Checking other dependencies...
python -c "import PIL" 2>nul
if errorlevel 1 (
    echo ✗ Pillow not installed
    echo Installing Pillow...
    pip install pillow
) else (
    echo ✓ Pillow is installed
)

python -c "import numpy" 2>nul
if errorlevel 1 (
    echo ✗ NumPy not installed
    echo Installing NumPy...
    pip install numpy
) else (
    echo ✓ NumPy is installed
)

python -c "import cv2" 2>nul
if errorlevel 1 (
    echo ✗ OpenCV not installed
    echo Installing OpenCV...
    pip install opencv-python
) else (
    echo ✓ OpenCV is installed
)

echo.
echo [CHECK 5] Port 5000 Availability
echo ================================================================
netstat -ano | findstr :5000 >nul
if errorlevel 1 (
    echo ✓ Port 5000 is available
) else (
    echo ✗ WARNING: Port 5000 is already in use
    echo.
    echo Another application is using port 5000.
    echo You may need to stop it or use a different port.
)

echo.
echo [CHECK 6] Firewall
echo ================================================================
echo If Windows Firewall blocks Python, allow it when prompted.

echo.
echo ================================================================
echo Diagnostic Complete!
echo ================================================================
echo.
echo Now attempting to start the application...
echo If it works, your browser should open to: http://localhost:5000
echo.
pause

echo.
echo Starting application...
echo.
start http://localhost:5000
python app.py

echo.
pause
