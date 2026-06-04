@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo Advanced Dataset Organization
echo ============================================================
echo.
echo This will deeply scan and organize your ECG dataset.
echo.
pause

echo.
echo [STEP 1] Running advanced dataset scanner...
echo ============================================================

cd /d "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"

REM Check if dataset folder exists
if not exist "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\Dataset" (
    echo.
    echo ERROR: Dataset folder not found at:
    echo C:\Users\VARUN COMPUTERS\Desktop\7th SEM\Dataset
    echo.
    echo Please check the folder location.
    pause
    exit /b 1
)

echo.
echo Scanning dataset structure...
dir "C:\Users\VARUN COMPUTERS\Desktop\7th SEM\Dataset" /s /b | findstr /i "\.png\|\.jpg\|\.jpeg\|\.bmp\|\.tiff\|\.tif" > temp_images.txt

if %errorlevel% equ 0 (
    echo Found image files:
    type temp_images.txt | findstr /n "^"
    del temp_images.txt
) else (
    echo No image files found in basic scan.
    del temp_images.txt
)

echo.
echo Running advanced Python scanner...
python advanced_dataset_organizer.py

if errorlevel 1 (
    echo.
    echo ERROR: Advanced scanning failed
    pause
    exit /b 1
)

echo.
echo [STEP 2] Training models...
echo ============================================================

if exist "models" (
    echo Models directory exists
) else (
    mkdir "models"
)

echo.
echo Starting model training...
python train_models.py

if errorlevel 1 (
    echo.
    echo WARNING: Training encountered issues
    echo The website will still work but predictions may not be optimal
)

echo.
echo [STEP 3] Starting website...
echo ============================================================
echo.
echo Starting website with your organized dataset...
echo Website will open at: http://localhost:5000
echo.
start http://localhost:5000
python app.py

echo.
echo Process complete.
pause
