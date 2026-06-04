@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo SIMPLE TEST - Heart Disease Analyzer
echo ============================================================
echo.
echo This will start a simplified version of the website to test
echo if the basic functionality works correctly.
echo.
pause

echo.
echo Starting simple test app...
echo ============================================================

cd /d "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"

REM Check if required packages are installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing Flask...
    pip install flask
)

echo.
echo Opening browser to: http://localhost:5000
start http://localhost:5000

echo.
echo Starting server...
echo Press Ctrl+C to stop
echo ============================================================

python simple_test_app.py

echo.
pause