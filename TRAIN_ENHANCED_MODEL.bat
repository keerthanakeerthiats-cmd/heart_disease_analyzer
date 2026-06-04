@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo ENHANCED MODEL TRAINING - Heart Disease Analyzer
echo ============================================================
echo.
echo This will train enhanced AI models with higher accuracy.
echo.
echo Estimated time: 2-4 hours (depending on dataset size and GPU)
echo.
pause

echo.
echo [STEP 1] Checking prerequisites...
echo ============================================================

cd /d "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"

REM Check if Python and TensorFlow are available
python -c "import sys; print('Python version:', sys.version)"
if errorlevel 1 (
    echo ❌ Python not found!
    pause
    exit /b 1
)

echo.
echo Checking TensorFlow...
python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__)"
if errorlevel 1 (
    echo ❌ TensorFlow not found!
    echo Installing TensorFlow CPU version...
    pip install tensorflow-cpu
    if errorlevel 1 (
        echo ❌ Failed to install TensorFlow
        pause
        exit /b 1
    )
)

echo.
echo Checking if dataset is organized...
if not exist "datasets\varun_ecg\train" (
    echo ⚠️  Dataset structure not found
    echo Creating dataset structure...
    python prepare_medical_dataset.py
    if errorlevel 1 (
        echo ❌ Failed to create dataset structure
        pause
        exit /b 1
    )
)

echo.
echo Checking if dataset has images...
set train_count=0
for /r "datasets\varun_ecg\train" %%f in (*) do set /a train_count+=1
if %train_count% == 0 (
    echo ⚠️  No images found in training dataset!
    echo.
    echo Please add medical images to your dataset folders:
    echo   datasets\varun_ecg\train\[condition]\*.jpg
    echo   datasets\varun_ecg\val\[condition]\*.jpg
    echo.
    echo Sample datasets can be downloaded from:
    echo   - Kaggle ECG Heartbeat Dataset
    echo   - PhysioNet MIT-BIH Arrhythmia Database
    echo.
    pause
    exit /b 1
)

echo.
echo [STEP 2] Training Enhanced Models...
echo ============================================================

echo Training enhanced models with improved architecture...
python train_enhanced_model.py

if errorlevel 1 (
    echo ❌ Training failed!
    pause
    exit /b 1
)

echo.
echo [STEP 3] Starting website with enhanced AI...
echo ============================================================

echo.
echo Enhanced models trained successfully!
echo Starting Heart Disease Analyzer with improved predictions...

start http://localhost:5000
python app.py

echo.
echo Press any key to exit...
pause