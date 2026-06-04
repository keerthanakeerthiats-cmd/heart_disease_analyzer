@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo Heart Disease Analyzer - Complete Diagnostic and Start
echo ============================================================
echo.
echo This tool will:
echo 1. Run complete diagnostics
echo 2. Start the fixed version on port 5001
echo.
pause

echo.
echo [STEP 1] Running Complete Diagnostics...
echo ============================================================

cd /d "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"

python website_diagnostic.py

echo.
echo Press any key to continue...
pause >nul

echo.
echo [STEP 2] Starting Fixed Version...
echo ============================================================

echo Opening browser to: http://localhost:5001
start http://localhost:5001

echo.
echo Server starting on port 5001...
echo Press Ctrl+C to stop
echo ============================================================

python app_fixed.py

echo.
pause