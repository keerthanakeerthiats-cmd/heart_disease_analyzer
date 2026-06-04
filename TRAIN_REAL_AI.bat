@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo REAL AI MODEL TRAINING - Heart Disease Analyzer
echo ============================================================
echo.
echo This will train real AI models for better predictions.
echo.
echo Estimated time: 1-3 hours (depending on dataset size)
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
if not exist "datasets\ecg\train" (
    echo ⚠️  ECG dataset not found in datasets\ecg\train
    echo Running dataset organizer...
    python organize_ecg_dataset.py
    if errorlevel 1 (
        echo ❌ Failed to organize dataset
        pause
        exit /b 1
    )
)

echo.
echo [STEP 2] Training ECG model...
echo ============================================================

python train_real_models.py
if errorlevel 1 (
    echo ❌ Training failed!
    pause
    exit /b 1
)

echo.
echo [STEP 3] Starting website with real AI...
echo ============================================================

echo.
echo Real AI models trained successfully!
echo Starting Heart Disease Analyzer with real predictions...

start http://localhost:5000
python app.py

echo.
echo Press any key to exit...
pause