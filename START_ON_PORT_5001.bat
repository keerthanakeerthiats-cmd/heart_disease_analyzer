@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo START HEART DISEASE ANALYZER - PORT 5001
echo ============================================================
echo.
echo This will start the website on the correct port (5001).
echo.
echo Access the website at: http://localhost:5001
echo.
pause

echo.
echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python and add it to PATH
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install -r requirements.txt

echo.
echo Starting the Heart Disease Analyzer on port 5001...
echo ============================================================

cd /d "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"

echo.
echo Opening browser to: http://localhost:5001
start http://localhost:5001

echo.
echo Starting Flask server on port 5001...
echo Press Ctrl+C to stop the server
echo ============================================================

python app.py

echo.
echo Server stopped.
pause