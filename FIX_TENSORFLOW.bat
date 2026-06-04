@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo TensorFlow Installation Fix
echo ============================================================
echo.
echo This script will fix TensorFlow installation issues.
echo.

echo [STEP 1] Checking current Python version...
echo ============================================================
python --version
echo.

echo [STEP 2] Uninstalling existing TensorFlow packages...
echo ============================================================
python -m pip uninstall tensorflow tensorflow-cpu tensorflow-gpu -y
echo.

echo [STEP 3] Cleaning up corrupted packages...
echo ============================================================
python -m pip cache purge
echo.

echo [STEP 4] Installing TensorFlow CPU (Windows compatible)...
echo ============================================================
python -m pip install tensorflow-cpu
echo.

echo [STEP 5] Verifying installation...
echo ============================================================
python -c "import tensorflow as tf; print('TensorFlow version:', tf.__version__); print('Installation successful!')"
echo.

echo ============================================================
echo TensorFlow Installation Fix Complete
echo ============================================================
echo.
echo If you still encounter issues, please restart your computer
echo and try running the Heart Disease Analyzer again.
echo.
pause