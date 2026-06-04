@echo off
echo ============================================================
echo Heart Disease Analyzer - Setup and Installation
echo ============================================================
echo.

echo Step 1: Installing basic dependencies...
pip install flask flask-cors pillow numpy opencv-python scikit-learn matplotlib
echo.

echo Step 2: Installing TensorFlow (this may take a while)...
echo Note: TensorFlow requires Python 3.8-3.11
echo.
pip install tensorflow
echo.

echo Step 3: Creating sample test images...
python create_samples.py
echo.

echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo To start the application:
echo   python app.py
echo.
echo Then open your browser to: http://localhost:5000
echo.
echo ============================================================
pause
