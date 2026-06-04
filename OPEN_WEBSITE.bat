@echo off
echo ============================================================
echo Starting Heart Disease Analyzer Website
echo ============================================================
echo.
echo The website will open at: http://localhost:5000
echo.
echo IMPORTANT:
echo   - Keep this window open while using the website
echo   - Press Ctrl+C to stop the server when done
echo   - Your browser may open automatically
echo.
echo ============================================================
echo.

REM Navigate to the script directory
cd /d "%~dp0"

echo Starting server...
echo.

REM Start the Flask app
start http://localhost:5000
python app.py

echo.
echo ============================================================
echo Server stopped.
echo ============================================================
echo.
pause
