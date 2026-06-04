@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo Starting Enhanced Heart Disease Analyzer
echo ============================================================
echo.
echo This version has better error handling and logging.
echo.
pause

echo.
echo [STEP 1] Checking if models exist...
echo ============================================================

cd /d "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"

if exist "models\ecg_model.h5" (
    echo ✅ ECG model found
) else (
    echo ⚠️  ECG model not found (will use mock predictions)
)

if exist "models\mri_model.h5" (
    echo ✅ MRI model found
) else (
    echo ⚠️  MRI model not found (will use mock predictions)
)

echo.
echo [STEP 2] Starting enhanced web application...
echo ============================================================

echo.
echo Starting server with better error handling...
echo Website will open at: http://localhost:5000
echo.
echo Also try: http://127.0.0.1:5000
echo Health check: http://localhost:5000/health
echo.
start http://localhost:5000
python app_enhanced.py

echo.
echo Server stopped.
pause
