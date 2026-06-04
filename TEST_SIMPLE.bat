@echo off
echo ============================================================
echo Testing Basic Server (No AI Models Needed)
echo ============================================================
echo.
echo This tests if Python and Flask work, without AI features.
echo.
pause

cd /d "%~dp0"

echo Installing Flask...
pip install flask flask-cors

echo.
echo Starting test server...
echo.
start http://localhost:5000
python test_server.py

pause
