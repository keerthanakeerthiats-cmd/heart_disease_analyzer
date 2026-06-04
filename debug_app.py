"""
Debug version of the Flask app with maximum error reporting
"""

import sys
import traceback
import logging

# Enable maximum logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

print("=" * 60)
print("DEBUG: Starting Heart Disease Analyzer")
print("=" * 60)
print()

try:
    print("1. Importing Flask...")
    from flask import Flask, render_template, request, jsonify
    print("   ✓ Flask imported successfully")
    
    print("2. Importing CORS...")
    from flask_cors import CORS
    print("   ✓ CORS imported successfully")
    
    print("3. Importing OS module...")
    import os
    print("   ✓ OS module imported successfully")
    
    print("4. Creating Flask app...")
    app = Flask(__name__)
    print("   ✓ Flask app created")
    
    print("5. Enabling CORS...")
    CORS(app)
    print("   ✓ CORS enabled")
    
    print("6. Setting up configuration...")
    UPLOAD_FOLDER = 'uploads'
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    print("   ✓ Configuration set")
    
    # Routes
    @app.route('/')
    def index():
        print("   DEBUG: Serving index route")
        return render_template('index.html')
    
    @app.route('/health')
    def health_check():
        print("   DEBUG: Serving health check")
        return {'status': 'healthy', 'debug': True}
    
    @app.route('/predict/ecg', methods=['POST'])
    def predict_ecg():
        print("   DEBUG: ECG prediction endpoint called")
        return jsonify({
            'prediction': 'Debug Mode',
            'confidence': 100.0,
            'message': 'App is working!'
        })
    
    print("7. All routes defined")
    
    print()
    print("8. Starting server...")
    print("   Access at: http://localhost:5000")
    print("   Health check: http://localhost:5000/health")
    print()
    
    app.run(debug=True, host='127.0.0.1', port=5000)
    
except Exception as e:
    print()
    print("❌ ERROR OCCURRED:")
    print(f"   {type(e).__name__}: {str(e)}")
    print()
    print("Full traceback:")
    traceback.print_exc()
    
    print()
    print("Press Enter to exit...")
    input()
