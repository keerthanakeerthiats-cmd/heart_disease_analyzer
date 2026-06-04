"""
Debug script to identify and fix website issues
"""

import os
import sys
import json
from pathlib import Path

def check_python_setup():
    """Check Python and package installations"""
    print("=" * 60)
    print("DEBUG: Python Environment Check")
    print("=" * 60)
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check required packages
    packages = ['flask', 'tensorflow', 'numpy', 'PIL', 'cv2']
    for package in packages:
        try:
            if package == 'PIL':
                import PIL
                print(f"✅ PIL (Pillow) version: {PIL.__version__}")
            elif package == 'cv2':
                import cv2
                print(f"✅ OpenCV version: {cv2.__version__}")
            else:
                __import__(package)
                print(f"✅ {package} available")
        except ImportError as e:
            print(f"❌ {package} not available: {e}")

def check_model_files():
    """Check if model files exist"""
    print("\n" + "=" * 60)
    print("DEBUG: Model Files Check")
    print("=" * 60)
    
    model_dir = Path("models")
    if model_dir.exists():
        print("✅ Models directory exists")
        for file in model_dir.iterdir():
            print(f"  - {file.name} ({file.stat().st_size} bytes)")
    else:
        print("⚠️ Models directory not found")
    
    # Check specific model files
    ecg_model = model_dir / "ecg_model.h5"
    mri_model = model_dir / "mri_model.h5"
    
    if ecg_model.exists():
        print(f"✅ ECG model found: {ecg_model}")
    else:
        print("⚠️ ECG model not found (will use mock predictions)")
        
    if mri_model.exists():
        print(f"✅ MRI model found: {mri_model}")
    else:
        print("⚠️ MRI model not found (will use mock predictions)")

def check_dataset_structure():
    """Check dataset organization"""
    print("\n" + "=" * 60)
    print("DEBUG: Dataset Structure Check")
    print("=" * 60)
    
    dataset_dirs = ["datasets/ecg/train", "datasets/ecg/validation", 
                   "datasets/mri/train", "datasets/mri/validation"]
    
    for dir_path in dataset_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ {dir_path} exists")
            # Count files in directory
            files = list(path.glob("*"))
            print(f"  Contains {len(files)} items")
            if files:
                print(f"  Sample: {files[0].name}")
        else:
            print(f"⚠️ {dir_path} not found")

def check_web_files():
    """Check web files"""
    print("\n" + "=" * 60)
    print("DEBUG: Web Files Check")
    print("=" * 60)
    
    required_files = ["templates/index.html", "app.py", "app_with_trained_models.py"]
    
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} not found")

def check_ports():
    """Check if port 5000 is available"""
    print("\n" + "=" * 60)
    print("DEBUG: Port Availability Check")
    print("=" * 60)
    
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 5000))
        sock.close()
        
        if result == 0:
            print("⚠️ Port 5000 is in use (this might be your running server)")
        else:
            print("✅ Port 5000 is available")
    except Exception as e:
        print(f"⚠️ Could not check port: {e}")

def run_diagnostics():
    """Run all diagnostics"""
    print("Heart Disease Analyzer - Diagnostic Tool")
    print("=" * 60)
    
    check_python_setup()
    check_model_files()
    check_dataset_structure()
    check_web_files()
    check_ports()
    
    print("\n" + "=" * 60)
    print("DEBUG COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("1. If models are missing, run TRAIN_REAL_AI.bat")
    print("2. If datasets are missing, run USE_YOUR_DATASET.bat")
    print("3. If packages are missing, install them with pip")
    print("4. If port is in use, stop other servers or change port")

if __name__ == "__main__":
    run_diagnostics()