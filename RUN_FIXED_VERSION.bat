@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo Heart Disease Analyzer - Fixed Version
echo ============================================================
echo.
echo This version uses port 5001 and has enhanced error handling.
echo.
pause

echo.
echo Starting Heart Disease Analyzer (Fixed Version)...
echo ============================================================

cd /d "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"

echo Opening browser to: http://localhost:5001
start http://localhost:5001

echo.
echo Server starting on port 5001...
echo Press Ctrl+C to stop
echo ============================================================

python app_fixed.py

echo.
pause