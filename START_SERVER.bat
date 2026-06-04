@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo START HEART DISEASE ANALYZER - RELIABLE VERSION
echo ============================================================
echo.
echo This will start the website with guaranteed compatibility.
echo.
echo Access the website at: http://localhost:5000
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
echo Installing required packages (without TensorFlow initially)...
pip install flask flask-cors pillow numpy opencv-python

echo.
echo Starting the Heart Disease Analyzer in compatibility mode...
echo ============================================================

cd /d "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"

echo.
echo Opening browser to: http://localhost:5000
start http://localhost:5000

echo.
echo Starting Flask server on port 5000...
echo Press Ctrl+C to stop the server
echo ============================================================

python app_no_ai.py

echo.
echo Server stopped.
pause