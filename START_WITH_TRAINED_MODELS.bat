@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo STARTING HEART DISEASE ANALYZER WITH TRAINED AI MODELS
echo ============================================================
echo.
echo This will start the website using your trained AI models.
echo.
pause

echo.
echo [STEP 1] Checking for trained models...
echo ============================================================

cd /d "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"

REM Check if models exist
if exist "models\ecg_model.h5" (
    echo ✅ ECG model found
) else (
    echo ⚠️  ECG model not found - will use mock predictions
)

if exist "models\mri_model.h5" (
    echo ✅ MRI model found
) else (
    echo ⚠️  MRI model not found - will use mock predictions
)

echo.
echo [STEP 2] Checking dependencies...
echo ============================================================

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo Please install Python 3.11 from https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
    echo ✅ %PYTHON_VERSION%
)

REM Check Flask
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Flask not found - installing...
    pip install flask
    if errorlevel 1 (
        echo ❌ Failed to install Flask
        pause
        exit /b 1
    )
) else (
    echo ✅ Flask available
)

REM Check TensorFlow (optional - for real AI)
python -c "import tensorflow" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  TensorFlow not found - website will use mock predictions
    echo To enable real AI predictions, install TensorFlow with:
    echo pip install tensorflow-cpu
) else (
    echo ✅ TensorFlow available
)

echo.
echo [STEP 3] Starting website...
echo ============================================================

echo.
echo Starting Heart Disease Analyzer...
echo Website will open at: http://localhost:5000
echo.

REM Open browser
start http://localhost:5000

REM Start server with trained models
python app_with_trained_models.py

echo.
echo Press any key to exit...
pause