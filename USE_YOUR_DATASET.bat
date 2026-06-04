@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo Training with Your ECG Dataset
echo ============================================================
echo.
echo Dataset Location: C:\Users\VARUN COMPUTERS\Desktop\7th SEM\Dataset
echo.
echo This will:
echo   1. Install TensorFlow (if needed)
echo   2. Organize your dataset
echo   3. Train AI models
echo   4. Start website with real predictions
echo.
pause

echo.
echo [STEP 1] Installing TensorFlow and dependencies...
echo ============================================================
pip install tensorflow scikit-learn matplotlib pillow opencv-python pandas numpy

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install packages
    echo Please make sure Python is installed correctly
    pause
    exit /b 1
)

echo.
echo [STEP 2] Organizing your dataset...
echo ============================================================

cd /d "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"

REM Check if dataset folders exist
if not exist "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\Dataset\archive" (
    echo.
    echo ERROR: Dataset folder not found at:
    echo C:\Users\VARUN COMPUTERS\Desktop\7th SEM\Dataset\archive
    pause
    exit /b 1
)

echo.
echo Found dataset folders:
dir "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\Dataset" /ad

echo.
echo Running dataset organizer...
python organize_ecg_dataset.py

echo.
echo [STEP 3] Training AI models...
echo ============================================================
echo This may take 1-3 hours depending on your dataset size.
echo Training progress will be shown below...
echo.

REM Create models directory if it doesn't exist
if not exist "models" mkdir "models"

python train_models.py

if errorlevel 1 (
    echo.
    echo WARNING: Training encountered issues
    echo The website will still work but predictions may not be optimal
    pause
)

echo.
echo [STEP 4] Starting website with real AI predictions...
echo ============================================================
echo.
echo Training complete! Starting website with your trained models...
echo.
echo Website will open at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server when done.
echo.
start http://localhost:5000
python app.py

echo.
echo Server stopped.
pause
