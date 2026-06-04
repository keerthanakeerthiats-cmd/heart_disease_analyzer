@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo HEART DISEASE ANALYZER - START WEBSITE NOW
echo ============================================================
echo.
echo This is the CORRECT way to start the website.
echo This version will work without TensorFlow issues.
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
echo Starting the Heart Disease Analyzer in COMPATIBILITY mode...
echo This uses app_no_ai.py which works without TensorFlow
echo ============================================================

cd /d "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"

echo.
echo Opening browser to: http://localhost:5000
start http://localhost:5000

echo.
echo Starting Flask server on port 5000...
echo NOTE: This version gives mock results but the UI works perfectly!
echo Press Ctrl+C to stop the server when done
echo ============================================================

python app_no_ai.py

echo.
echo Server stopped.
echo.
echo To use real AI predictions later, install TensorFlow:
echo pip install tensorflow
echo Then run: python app.py
pause