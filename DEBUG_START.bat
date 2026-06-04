@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo DEBUG: Heart Disease Analyzer Startup
echo ============================================================
echo.
echo This will show detailed startup information.
echo.
pause

echo.
echo [DEBUG STEP 1] Checking Python and dependencies...
echo ============================================================

python --version
if errorlevel 1 (
    echo ❌ Python not found!
    pause
    exit /b 1
)

echo.
echo Checking Flask...
python -c "import flask; print('✓ Flask version:', flask.__version__)"
if errorlevel 1 (
    echo ❌ Flask not installed
    echo Installing Flask...
    pip install flask
)

echo.
echo Checking CORS...
python -c "import flask_cors; print('✓ Flask-CORS available')"
if errorlevel 1 (
    echo ❌ Flask-CORS not installed
    echo Installing Flask-CORS...
    pip install flask-cors
)

echo.
echo Checking PIL...
python -c "from PIL import Image; print('✓ PIL available')"
if errorlevel 1 (
    echo ❌ PIL not installed
    echo Installing PIL...
    pip install pillow
)

echo.
echo [DEBUG STEP 2] Checking templates...
echo ============================================================

if exist "templates\index.html" (
    echo ✅ Found templates\index.html
) else (
    echo ❌ templates\index.html not found!
)

echo.
echo [DEBUG STEP 3] Running debug app...
echo ============================================================

echo.
echo Starting debug version with maximum error reporting...
echo.
python debug_app.py

echo.
echo Debug session ended.
pause
