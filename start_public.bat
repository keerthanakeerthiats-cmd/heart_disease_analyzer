@echo off
REM Start server in venv and provide guidance for exposing publicly
setlocal

:: Activate virtualenv if present
if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
) else (
    echo Virtual environment not found. Creating one...
    python -m venv .venv
    call ".venv\Scripts\activate.bat"
    python -m pip install --upgrade pip
    pip install -r requirements.txt
)
echo Starting Flask app on port 5001...
start "Flask" cmd /k "cd /d %~dp0 && python app.py"
echo.
echo The app will be available locally at: http://localhost:5001
for /f "tokens=2 delims= " %%i in ('ipconfig ^| findstr /R "IPv4 Address"') do set LAN_IP=%%i
if defined LAN_IP (
    echo And on your LAN at: http://%LAN_IP%:5001
) else (
    echo Could not detect LAN IP automatically; check with `ipconfig`.
)
echo.
echo To expose to the internet you can use ngrok (recommended):
echo 1) Download ngrok from https://ngrok.com/download and unzip to this folder or install system-wide.
echo 2) (Optional) Login and set your authtoken: `ngrok authtoken YOUR_TOKEN`
echo 3) Run: `ngrok http 5001` in a separate terminal. The public URL will be shown by ngrok.
echo.
echo Alternatively, set up port forwarding on your router for TCP port 5001 to this machine's LAN IP.
echo.
echo NOTE: To allow incoming connections on Windows Firewall run PowerShell as Administrator and execute:
echo New-NetFirewallRule -DisplayName "HeartAnalyzer5001" -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow
echo.
echo Press any key to exit.
pause >nul
