@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo Heart Disease Analyzer - No TensorFlow Version
echo ============================================================
echo.
echo This version works without TensorFlow for testing purposes.
echo.
pause

echo.
echo Starting Heart Disease Analyzer (No TensorFlow)...
echo ============================================================

cd /d "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"

echo Opening browser to: http://localhost:5000
start http://localhost:5000

echo.
echo Server starting...
echo Press Ctrl+C to stop
echo ============================================================

python app_no_tensorflow.py

echo.
pause