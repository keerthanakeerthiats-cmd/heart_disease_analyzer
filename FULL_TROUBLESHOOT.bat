@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo HEART DISEASE ANALYZER - COMPREHENSIVE TROUBLESHOOTING
echo ============================================================
echo.
echo This tool will help diagnose and fix the JavaScript error.
echo.
pause

echo.
echo [STEP 1] Running System Diagnostics...
echo ============================================================

cd /d "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"

if exist "RUN_DIAGNOSTICS.bat" (
    echo Running system diagnostics...
    call RUN_DIAGNOSTICS.bat
    echo.
    echo Press any key to continue...
    pause >nul
)

echo.
echo [STEP 2] Testing JavaScript Functionality...
echo ============================================================

echo Opening JavaScript error test in your browser...
start "" "js_error_test.html"

echo.
echo Please check your browser for the JavaScript test results.
echo Look for any FAILED tests (marked in red).
echo.
echo Press any key to continue...
pause >nul

echo.
echo [STEP 3] Testing with Simple Version...
echo ============================================================

echo Starting simple test version...
echo This will open in your browser automatically.
echo.
echo Close this window to stop the server.
echo.

start http://localhost:5000
python simple_test_app.py

echo.
echo ============================================================
echo TROUBLESHOOTING COMPLETE
echo ============================================================
echo.
echo If you're still experiencing issues:
echo 1. Check the browser console for errors (F12)
echo 2. Check the server console for errors
echo 3. Refer to TROUBLESHOOTING_JS_ERRORS.md for detailed help
echo.
pause