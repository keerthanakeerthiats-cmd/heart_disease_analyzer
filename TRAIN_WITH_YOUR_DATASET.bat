@echo off
echo ============================================================
echo ECG Dataset Training Setup
echo ============================================================
echo.
echo This will organize your ECG dataset and train AI models.
echo.
pause

echo.
echo [STEP 1] Installing required packages...
echo ============================================================
pip install tensorflow scikit-learn matplotlib pillow opencv-python

echo.
echo [STEP 2] Organizing ECG dataset...
echo ============================================================
python organize_ecg_dataset.py

echo.
echo [STEP 3] Training AI models...
echo ============================================================
echo This may take 1-3 hours depending on your dataset size.
echo.
python train_models.py

echo.
echo [STEP 4] Starting website with real AI...
echo ============================================================
echo Training complete! Starting website...
echo.
start http://localhost:5000
python app.py

pause
