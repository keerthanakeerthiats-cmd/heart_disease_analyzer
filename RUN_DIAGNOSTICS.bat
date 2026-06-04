@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo Heart Disease Analyzer - Diagnostic Tool
echo ============================================================
echo.
echo This will check your setup and identify potential issues.
echo.
pause

echo.
echo Running diagnostics...
echo ============================================================

cd /d "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"

python debug_website.py

echo.
echo ============================================================
echo Diagnostic Complete
echo ============================================================
echo.
echo Check the output above for any issues marked with ❌
echo.
echo Common solutions:
echo - If TensorFlow is missing: pip install tensorflow-cpu
echo - If OpenCV is missing: pip install opencv-python
echo - If Pillow is missing: pip install Pillow
echo - If Flask is missing: pip install flask
echo.
echo After fixing issues, run this diagnostic again to confirm.
echo.
pause