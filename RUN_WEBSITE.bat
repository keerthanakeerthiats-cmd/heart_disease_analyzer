@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo RUN HEART DISEASE ANALYZER WEBSITE - EASIEST METHOD
echo ============================================================
echo.
echo This is the EASIEST and most reliable way to run the website.
echo.
echo WEBSITE WILL BE AVAILABLE AT: http://localhost:5000
echo.
echo The results page will be at: http://localhost:5000/results
echo ============================================================
pause

echo.
echo Checking if Python is available...
python --version
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo SOLUTION:
    echo 1. Download Python from https://www.python.org/downloads/
    echo 2. During installation, CHECK "Add Python to PATH"
    echo 3. Restart your computer
    echo 4. Run this file again
    echo.
    pause
    exit /b 1
)

echo.
echo Installing required packages...
echo (This may take a few minutes on first run)
pip install flask flask-cors pillow numpy opencv-python

echo.
echo ============================================================
echo STARTING WEBSITE NOW...
echo ============================================================

cd /d "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"

echo.
echo Opening your web browser automatically...
start http://localhost:5000

echo.
echo Launching the Heart Disease Analyzer...
echo.
echo IMPORTANT NOTES:
echo - The website will work perfectly with mock results
echo - This avoids TensorFlow compatibility issues
echo - All pages (main, results, accuracy) will be accessible
echo - Keep this window open while using the website
echo - Press Ctrl+C in this window to stop the server
echo ============================================================

python app_no_ai.py

echo.
echo Server has stopped.
echo You can run this file again anytime to restart the website.
pause