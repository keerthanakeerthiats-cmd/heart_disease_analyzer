"""
Website Error Diagnostic Tool
"""

import os
import sys
import json
from pathlib import Path

def check_website_files():
    """Check if all required website files exist"""
    print("=" * 60)
    print("WEBSITE FILES CHECK")
    print("=" * 60)
    
    # Check templates directory and index.html
    templates_dir = Path("templates")
    index_html = templates_dir / "index.html"
    
    if templates_dir.exists():
        print("✅ templates directory exists")
        if index_html.exists():
            print("✅ templates/index.html exists")
            # Check file size
            size = index_html.stat().st_size
            print(f"   File size: {size} bytes")
        else:
            print("❌ templates/index.html NOT found")
    else:
        print("❌ templates directory NOT found")
    
    # Check app files
    app_files = ["app.py", "app_no_tensorflow.py", "app_enhanced.py"]
    for app_file in app_files:
        if Path(app_file).exists():
            print(f"✅ {app_file} exists")
        else:
            print(f"❌ {app_file} NOT found")

def check_uploads_directory():
    """Check uploads directory"""
    print("\n" + "=" * 60)
    print("UPLOADS DIRECTORY CHECK")
    print("=" * 60)
    
    uploads_dir = Path("uploads")
    if uploads_dir.exists():
        print("✅ uploads directory exists")
        # Check if writable
        try:
            test_file = uploads_dir / "test.txt"
            test_file.write_text("test")
            test_file.unlink()
            print("✅ uploads directory is writable")
        except Exception as e:
            print(f"❌ uploads directory NOT writable: {e}")
    else:
        print("⚠️ uploads directory NOT found (will be created when needed)")

def check_python_packages():
    """Check required Python packages"""
    print("\n" + "=" * 60)
    print("PYTHON PACKAGES CHECK")
    print("=" * 60)
    
    required_packages = ["flask", "json", "os", "random"]
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} available")
        except ImportError as e:
            print(f"❌ {package} NOT available: {e}")

def check_port_availability():
    """Check if port 5000 is available"""
    print("\n" + "=" * 60)
    print("PORT AVAILABILITY CHECK")
    print("=" * 60)
    
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 5000))
        sock.close()
        
        if result == 0:
            print("⚠️ Port 5000 is IN USE (might be another server running)")
        else:
            print("✅ Port 5000 is AVAILABLE")
    except Exception as e:
        print(f"⚠️ Could not check port: {e}")

def run_diagnostics():
    """Run all diagnostics"""
    print("Heart Disease Analyzer - Website Error Diagnostic")
    print("=" * 60)
    
    check_website_files()
    check_uploads_directory()
    check_python_packages()
    check_port_availability()
    
    print("\n" + "=" * 60)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Check if all required files exist (marked with ✅)")
    print("2. Ensure uploads directory is writable")
    print("3. Verify all required packages are installed")
    print("4. Check if port 5000 is available")
    print("\nIf issues persist:")
    print("- Try running RUN_NO_TENSORFLOW.bat")
    print("- Check browser console for JavaScript errors (F12)")
    print("- Check server console for Python errors")

if __name__ == "__main__":
    run_diagnostics()