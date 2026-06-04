@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo Analyzing Your ECG Dataset (No TensorFlow Required)
echo ============================================================
echo.
echo This will organize your dataset for future training.
echo.
pause

echo.
echo [STEP 1] Analyzing and organizing your dataset...
echo ============================================================

cd /d "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"

REM Check if dataset folder exists
if not exist "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\Dataset" (
    echo.
    echo ERROR: Dataset folder not found at:
    echo C:\Users\VARUN COMPUTERS\Desktop\7th SEM\Dataset
    echo.
    echo Please make sure your dataset is in the correct location.
    pause
    exit /b 1
)

echo.
echo Found dataset folders:
dir "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\Dataset" /ad

echo.
echo Running dataset analyzer (no TensorFlow needed)...
python analyze_dataset_no_tf.py

if errorlevel 1 (
    echo.
    echo ERROR: Dataset analysis failed
    pause
    exit /b 1
)

echo.
echo [STEP 2] Trying to fix TensorFlow...
echo ============================================================

echo.
echo Attempting to install CPU-only TensorFlow...
pip uninstall tensorflow -y
pip install tensorflow-cpu

if errorlevel 1 (
    echo.
    echo WARNING: Could not install TensorFlow
    echo Your dataset is organized and ready for later training
    echo.
    echo When you fix TensorFlow, run: python train_models.py
) else (
    echo.
    echo SUCCESS: TensorFlow installed!
    echo.
    echo Now training models with your dataset...
    python train_models.py
)

echo.
echo [STEP 3] Starting website...
echo ============================================================
echo.
echo Starting website with organized dataset...
echo Website will open at: http://localhost:5000
echo.
start http://localhost:5000
python app.py

echo.
echo Process complete.
pause
