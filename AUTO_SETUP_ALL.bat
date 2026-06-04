@echo off
setlocal enabledelayedexpansion

echo.
echo ================================================================
echo    HEART DISEASE ANALYZER - COMPLETE AUTOMATED SETUP
echo ================================================================
echo.
echo This script will:
echo   1. Setup Kaggle API credentials
echo   2. Download ECG dataset from Kaggle (109,446 samples)
echo   3. Prepare dataset (convert to images)
echo   4. Train AI models (ECG + MRI)
echo   5. Start the web application
echo.
echo TOTAL TIME: Approximately 2-3 hours
echo.
echo ================================================================
echo.

pause

echo.
echo [STEP 1/5] Setting up Kaggle API...
echo ================================================================
echo.

REM Create .kaggle directory
if not exist "%USERPROFILE%\.kaggle" (
    mkdir "%USERPROFILE%\.kaggle"
    echo Created: %USERPROFILE%\.kaggle
) else (
    echo Directory already exists
)

REM Check for kaggle.json
if exist "%USERPROFILE%\Downloads\kaggle.json" (
    echo Found kaggle.json in Downloads!
    move /Y "%USERPROFILE%\Downloads\kaggle.json" "%USERPROFILE%\.kaggle\kaggle.json"
    echo Moved to correct location
) else (
    if exist "%USERPROFILE%\.kaggle\kaggle.json" (
        echo kaggle.json already in place
    ) else (
        echo.
        echo ================================================================
        echo ERROR: kaggle.json NOT FOUND!
        echo ================================================================
        echo.
        echo Please download kaggle.json first:
        echo   1. Go to https://www.kaggle.com/
        echo   2. Login and go to Settings
        echo   3. Scroll to API section
        echo   4. Click "Create New API Token"
        echo   5. Save to Downloads folder
        echo   6. Run this script again
        echo.
        pause
        exit /b 1
    )
)

echo.
echo Installing required packages...
pip install kaggle --quiet
pip install --upgrade pip --quiet

echo.
echo Testing Kaggle API...
python test_kaggle.py

if errorlevel 1 (
    echo.
    echo ERROR: Kaggle API test failed!
    echo Please check your kaggle.json file.
    pause
    exit /b 1
)

echo.
echo [STEP 2/5] Downloading Dataset from Kaggle...
echo ================================================================
echo This may take 10-20 minutes depending on your internet speed.
echo.

python prepare_kaggle_dataset.py

if errorlevel 1 (
    echo.
    echo ERROR: Dataset download failed!
    pause
    exit /b 1
)

echo.
echo [STEP 3/5] Creating Sample Test Images...
echo ================================================================
echo.

python create_samples.py

echo.
echo [STEP 4/5] Training AI Models...
echo ================================================================
echo This will take 1-3 hours. You can leave this running.
echo Progress will be shown below...
echo.

set /p TRAIN="Do you want to train models now? (y/n): "

if /i "%TRAIN%"=="y" (
    echo.
    echo Starting training... Please be patient.
    python train_models.py
    
    if errorlevel 1 (
        echo.
        echo WARNING: Training encountered errors or was incomplete.
        echo The app will still work but predictions may not be accurate.
        pause
    )
) else (
    echo.
    echo Skipping training. Models will be untrained (random predictions).
)

echo.
echo [STEP 5/5] Starting Web Application...
echo ================================================================
echo.
echo Your Heart Disease Analyzer is ready!
echo.
echo The website will open at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server when done.
echo.
pause

echo.
echo Starting server...
python app.py

echo.
echo ================================================================
echo Server stopped.
echo ================================================================
echo.
pause
