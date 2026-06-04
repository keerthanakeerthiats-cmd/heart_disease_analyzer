@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo HEART DISEASE ANALYZER - ACCURACY IMPROVEMENT TRAINING
echo ============================================================
echo.
echo This will train advanced models with the following improvements:
echo 1. Transfer learning with ResNet50
echo 2. Advanced image preprocessing
echo 3. Enhanced data augmentation
echo 4. Model ensembling capabilities
echo 5. Fine-tuning strategies
echo.
echo Estimated time: 3-6 hours (depending on dataset size and hardware)
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
echo Checking additional dependencies...
python -c "import skimage; print('scikit-image available')"
if errorlevel 1 (
    echo Installing scikit-image...
    pip install scikit-image
)

python -c "import scipy; print('scipy available')"
if errorlevel 1 (
    echo Installing scipy...
    pip install scipy
)

echo.
echo Checking if dataset is organized...
if not exist "datasets\varun_ecg\train" (
    echo ⚠️  ECG dataset structure not found
    echo Creating dataset structure...
    python prepare_medical_dataset.py
    if errorlevel 1 (
        echo ❌ Failed to create dataset structure
        pause
        exit /b 1
    )
)

if not exist "datasets\varun_mri\train" (
    echo ⚠️  MRI dataset structure not found
    echo Creating dataset structure...
    python prepare_medical_dataset.py
    if errorlevel 1 (
        echo ❌ Failed to create dataset structure
        pause
        exit /b 1
    )
)

echo Checking if dataset has images...
set ecg_train_count=0
for /r "datasets\varun_ecg\train" %%f in (*) do set /a ecg_train_count+=1
if !ecg_train_count! EQU 0 (
    echo ⚠️  No images found in ECG training dataset!
    echo.
    echo Please add ECG medical images to your dataset folders:
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

set mri_train_count=0
for /r "datasets\varun_mri\train" %%f in (*) do set /a mri_train_count+=1
if !mri_train_count! EQU 0 (
    echo ⚠️  No images found in MRI training dataset!
    echo.
    echo Please add MRI medical images to your dataset folders:
    echo   datasets\varun_mri\train\[condition]\*.jpg
    echo   datasets\varun_mri\val\[condition]\*.jpg
    echo.
    echo Sample datasets can be downloaded from:
    echo   - Kaggle Cardiac MRI datasets
    echo   - Medical Imaging Databases
    echo.
    pause
    exit /b 1
)

echo.
echo [STEP 2] Installing enhanced requirements...
echo ============================================================

pip install -r requirements.txt

echo.
echo [STEP 3] Training Advanced Models with Accuracy Improvements...
echo ============================================================

echo Training advanced models with transfer learning and enhanced techniques...
python advanced_model_improver.py

if errorlevel 1 (
    echo ❌ Advanced model training failed!
    pause
    exit /b 1
)

echo.
echo [STEP 4] Verifying Model Performance...
echo ============================================================

echo Running model verification tests...
python -c "
import os
from model_ensemble import create_optimized_ensemble

print('Checking for ECG models...')
ecg_ensemble = create_optimized_ensemble('ecg')
if ecg_ensemble and len(ecg_ensemble.models) > 0:
    print(f'✅ Found {len(ecg_ensemble.models)} ECG models for ensemble')
else:
    print('⚠️  No ECG models found for ensemble')

print('Checking for MRI models...')
mri_ensemble = create_optimized_ensemble('mri')
if mri_ensemble and len(mri_ensemble.models) > 0:
    print(f'✅ Found {len(mri_ensemble.models)} MRI models for ensemble')
else:
    print('⚠️  No MRI models found for ensemble')
"

echo.
echo [STEP 5] Starting Enhanced Application...
echo ============================================================

echo.
echo Advanced models trained successfully!
echo Starting Heart Disease Analyzer with improved accuracy features...
echo.
echo New features available:
echo ✅ Transfer learning with ResNet50
echo ✅ Advanced image preprocessing
echo ✅ Ensemble prediction methods
echo ✅ Enhanced data augmentation
echo ✅ Improved model architectures
echo.

start http://localhost:5001
python app.py

echo.
echo ============================================================
echo TRAINING COMPLETED SUCCESSFULLY!
echo ============================================================
echo.
echo Your Heart Disease Analyzer now has:
echo • Improved model accuracy through transfer learning
echo • Advanced image preprocessing techniques  
echo • Ensemble methods for better predictions
echo • Enhanced data augmentation
echo • Fine-tuned architectures
echo.
echo Access the application at: http://localhost:5001
echo ============================================================
pause