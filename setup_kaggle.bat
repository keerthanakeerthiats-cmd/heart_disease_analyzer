@echo off
echo ============================================================
echo Kaggle API Setup - Automatic Configuration
echo ============================================================
echo.

echo Step 1: Creating .kaggle directory...
if not exist "%USERPROFILE%\.kaggle" (
    mkdir "%USERPROFILE%\.kaggle"
    echo Created: %USERPROFILE%\.kaggle
) else (
    echo Directory already exists: %USERPROFILE%\.kaggle
)
echo.

echo Step 2: Looking for kaggle.json in Downloads folder...
if exist "%USERPROFILE%\Downloads\kaggle.json" (
    echo Found kaggle.json in Downloads!
    
    echo.
    echo Step 3: Moving kaggle.json to .kaggle directory...
    move /Y "%USERPROFILE%\Downloads\kaggle.json" "%USERPROFILE%\.kaggle\kaggle.json"
    
    if exist "%USERPROFILE%\.kaggle\kaggle.json" (
        echo Success! kaggle.json moved to correct location.
    ) else (
        echo Error: Failed to move file.
    )
) else (
    echo.
    echo WARNING: kaggle.json NOT found in Downloads folder!
    echo.
    echo Please make sure you have:
    echo 1. Downloaded kaggle.json from Kaggle.com
    echo 2. The file is in your Downloads folder
    echo.
    echo Manual instructions:
    echo 1. Go to https://www.kaggle.com/
    echo 2. Click Profile Picture -^> Settings
    echo 3. Scroll to API section
    echo 4. Click "Create New API Token"
    echo 5. File will download to Downloads folder
    echo 6. Run this script again
    echo.
    pause
    exit /b 1
)

echo.
echo Step 4: Installing Kaggle API library...
pip install kaggle
echo.

echo Step 5: Testing Kaggle API setup...
python test_kaggle.py
echo.

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Your kaggle.json is now at:
echo %USERPROFILE%\.kaggle\kaggle.json
echo.
echo Next steps:
echo   1. Download dataset: python prepare_kaggle_dataset.py
echo   2. Train models:     python train_models.py
echo   3. Start app:        python app.py
echo.
pause
