@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo HEART DISEASE ANALYZER - WEBSITE ERROR DIAGNOSIS
echo ============================================================
echo.
echo Running diagnostic checks...
echo.

cd /d "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"

echo [CHECK 1] Python Installation
echo -------------------------------
python --version
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python and add it to PATH
    goto error_section
) else (
    echo ✅ Python is installed
)

echo.
echo [CHECK 2] Required Dependencies
echo -------------------------------
echo Checking for Flask...
python -c "import flask; print('Flask version:', flask.__version__)"
if errorlevel 1 (
    echo ❌ Flask not installed
    set flask_error=1
) else (
    echo ✅ Flask is installed
)

echo.
echo Checking for TensorFlow...
python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"
if errorlevel 1 (
    echo ❌ TensorFlow not installed
    set tf_error=1
) else (
    echo ✅ TensorFlow is installed
)

echo.
echo Checking for OpenCV...
python -c "import cv2; print('OpenCV version:', cv2.__version__)"
if errorlevel 1 (
    echo ❌ OpenCV not installed
    set cv2_error=1
) else (
    echo ✅ OpenCV is installed
)

echo.
echo Checking for NumPy...
python -c "import numpy; print('NumPy version:', numpy.__version__)"
if errorlevel 1 (
    echo ❌ NumPy not installed
    set numpy_error=1
) else (
    echo ✅ NumPy is installed
)

echo.
echo [CHECK 3] Model Files
echo ---------------------
if exist "models\ecg_model.h5" (
    echo ✅ ECG model file found
    set ecg_model_found=1
) else (
    echo ⚠️  ECG model file NOT found
)

if exist "models\mri_model.h5" (
    echo ✅ MRI model file found
    set mri_model_found=1
) else (
    echo ⚠️  MRI model file NOT found
)

if exist "models\enhanced_ecg_model.h5" (
    echo ✅ Enhanced ECG model file found
    set enhanced_ecg_model_found=1
) else (
    echo ⚠️  Enhanced ECG model file NOT found
)

if exist "models\enhanced_mri_model.h5" (
    echo ✅ Enhanced MRI model file found
    set enhanced_mri_model_found=1
) else (
    echo ⚠️  Enhanced MRI model file NOT found
)

echo.
echo [CHECK 4] Directory Structure
echo -------------------------------
if exist "templates" (
    echo ✅ Templates directory found
) else (
    echo ❌ Templates directory NOT found
    set templates_error=1
)

if exist "static" (
    echo ✅ Static directory found
) else (
    echo ⚠️  Static directory NOT found (may not be critical)
)

echo.
echo [CHECK 5] Port Availability
echo ---------------------------
echo Checking if port 5001 is available...
netstat -an | findstr :5001
if not errorlevel 1 (
    echo ⚠️  Port 5001 is in use
    echo This might cause the application to fail to start
    set port_error=1
) else (
    echo ✅ Port 5001 is available
)

echo.
echo [SUMMARY]
echo =========
echo Dependencies:
if defined flask_error (echo ❌ Flask not installed) else (echo ✅ Flask OK)
if defined tf_error (echo ❌ TensorFlow not installed) else (echo ✅ TensorFlow OK)
if defined cv2_error (echo ❌ OpenCV not installed) else (echo ✅ OpenCV OK)
if defined numpy_error (echo ❌ NumPy not installed) else (echo ✅ NumPy OK)

echo.
echo Models:
if defined ecg_model_found (echo ✅ ECG model available) else (echo ⚠️  ECG model missing)
if defined mri_model_found (echo ✅ MRI model available) else (echo ⚠️  MRI model missing)
if defined enhanced_ecg_model_found (echo ✅ Enhanced ECG model available) else (echo ⚠️  Enhanced ECG model missing)
if defined enhanced_mri_model_found (echo ✅ Enhanced MRI model available) else (echo ⚠️  Enhanced MRI model missing)

echo.
echo Potential Issues Found:
if defined templates_error (echo - Missing templates directory)
if defined port_error (echo - Port 5001 is in use)
if defined flask_error (echo - Missing Flask dependency)
if defined tf_error (echo - Missing TensorFlow dependency)
if defined cv2_error (echo - Missing OpenCV dependency)
if defined numpy_error (echo - Missing NumPy dependency)

if not defined flask_error if not defined tf_error if not defined cv2_error if not defined numpy_error if defined ecg_model_found if defined mri_model_found if not defined templates_error (
    echo.
    echo No major issues detected! Attempting to start the application...
    echo.
    goto start_app
) else (
    echo.
    echo Issues detected. Attempting to fix common problems...
    echo.
    goto fix_common_issues
)

:fix_common_issues
echo Installing missing dependencies...
pip install -r requirements.txt

if defined templates_error (
    echo Templates directory missing. Checking if files exist separately...
    dir templates\*.html
    if errorlevel 1 (
        echo No template files found. This is a critical issue.
        goto error_section
    )
)

if defined port_error (
    echo Killing processes on port 5001...
    netstat -ano | findstr :5001 > temp_port_check.txt
    for /f "tokens=5" %%a in ('type temp_port_check.txt ^| findstr LISTENING') do (
        echo Killing process %%a
        taskkill /pid %%a /f
    )
    del temp_port_check.txt
)

goto start_app

:start_app
echo.
echo [ATTEMPTING TO START APPLICATION]
echo ==================================
echo Starting Heart Disease Analyzer...
echo Access the application at: http://localhost:5001
echo.
echo Press Ctrl+C to stop the server
echo.
python app.py

goto end

:error_section
echo.
echo Critical errors detected. Cannot start the application.
echo Please fix the issues above and try again.
echo.

:end
echo.
echo Diagnostic complete.
pause