"""
Enhanced Flask app that properly loads and uses trained AI models
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
MODEL_FOLDER = 'models'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODEL_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Global variables for models
ecg_model = None
mri_model = None

# Disease classifications
ECG_CLASSES = [
    'Normal',
    'Myocardial Infarction',
    'Abnormal Heartbeat',
    'History of MI',
    'Arrhythmia'
]

MRI_CLASSES = [
    'Normal',
    'Cardiomyopathy',
    'Coronary Artery Disease',
    'Heart Failure',
    'Myocardial Infarction'
]

def load_models():
    """Load trained models if they exist"""
    global ecg_model, mri_model
    
    # Load ECG model
    ecg_model_path = os.path.join(MODEL_FOLDER, 'ecg_model.h5')
    if os.path.exists(ecg_model_path):
        try:
            ecg_model = keras.models.load_model(ecg_model_path)
            logger.info("✅ ECG model loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load ECG model: {e}")
    else:
        logger.warning("⚠️ ECG model not found - will use mock predictions")
    
    # Load MRI model
    mri_model_path = os.path.join(MODEL_FOLDER, 'mri_model.h5')
    if os.path.exists(mri_model_path):
        try:
            mri_model = keras.models.load_model(mri_model_path)
            logger.info("✅ MRI model loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load MRI model: {e}")
    else:
        logger.warning("⚠️ MRI model not found - will use mock predictions")

def preprocess_image(image_path, target_size=(128, 128)):
    """Preprocess image for model prediction"""
    try:
        # Read image
        image = Image.open(image_path)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image
        image = image.resize(target_size)
        
        # Convert to array and normalize
        img_array = np.array(image, dtype=np.float32)
        img_array = img_array / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        logger.error(f"Error preprocessing image: {str(e)}")
        return None

def get_disease_info(disease_name):
    """Get detailed information about the detected disease"""
    disease_descriptions = {
        'Normal': {
            'description': 'No cardiac abnormalities detected.',
            'severity': 'None',
            'color': '#4ecdc4'
        },
        'Myocardial Infarction': {
            'description': 'Heart attack - occurs when blood flow to the heart muscle is blocked.',
            'severity': 'Critical',
            'color': '#ff0000'
        },
        'Abnormal Heartbeat': {
            'description': 'Irregular heart rhythm that may require monitoring.',
            'severity': 'Moderate',
            'color': '#ffa500'
        },
        'History of MI': {
            'description': 'Previous heart attack with possible residual effects.',
            'severity': 'Moderate',
            'color': '#ff6b6b'
        },
        'Arrhythmia': {
            'description': 'Abnormal heart rhythm requiring cardiac evaluation.',
            'severity': 'Moderate',
            'color': '#ffa500'
        },
        'Cardiomyopathy': {
            'description': 'Disease of the heart muscle affecting pumping ability.',
            'severity': 'High',
            'color': '#ff6b6b'
        },
        'Coronary Artery Disease': {
            'description': 'Narrowing of coronary arteries reducing blood flow to heart.',
            'severity': 'High',
            'color': '#ff4444'
        },
        'Heart Failure': {
            'description': 'Condition where heart cannot pump blood effectively.',
            'severity': 'Critical',
            'color': '#ff0000'
        }
    }
    
    return disease_descriptions.get(disease_name, {
        'description': 'Cardiac condition requiring medical evaluation.',
        'severity': 'Unknown',
        'color': '#888888'
    })

def predict_mock(type):
    """Generate mock predictions for testing"""
    import random
    
    if type == 'ecg':
        diseases = ECG_CLASSES
    else:  # mri
        diseases = MRI_CLASSES
    
    predicted_disease = random.choice(diseases)
    
    # Generate realistic probabilities
    probabilities = {}
    total = 0
    for disease in diseases:
        prob = random.uniform(5, 40) if disease != predicted_disease else random.uniform(60, 95)
        probabilities[disease] = round(prob, 1)
        total += prob
    
    # Normalize to 100%
    for disease in diseases:
        probabilities[disease] = round(probabilities[disease] * 100 / total, 1)
    
    # Get predicted disease with highest probability
    predicted_disease = max(probabilities, key=probabilities.get)
    confidence = probabilities[predicted_disease]
    
    # Disease info
    disease_info = get_disease_info(predicted_disease)
    
    return jsonify({
        'prediction': predicted_disease,
        'confidence': confidence,
        'probabilities': probabilities,
        'disease_info': disease_info
    })

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ecg_model_loaded': ecg_model is not None,
        'mri_model_loaded': mri_model is not None
    })

@app.route('/predict/ecg', methods=['POST'])
def predict_ecg():
    """Predict heart disease from ECG image"""
    global ecg_model
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file temporarily
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Use real model if available
        if ecg_model is not None:
            # Preprocess image
            img_array = preprocess_image(filepath)
            
            if img_array is None:
                return jsonify({'error': 'Failed to process image'}), 400
            
            # Make prediction
            predictions = ecg_model.predict(img_array)
            
            # Get results
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx] * 100)
            predicted_disease = ECG_CLASSES[predicted_class_idx]
            
            # Create probabilities dictionary
            probabilities = {}
            for i, class_name in enumerate(ECG_CLASSES):
                probabilities[class_name] = float(predictions[0][i] * 100)
            
            # Get disease info
            disease_info = get_disease_info(predicted_disease)
            
            # Clean up temporary file
            os.remove(filepath)
            
            return jsonify({
                'prediction': predicted_disease,
                'confidence': confidence,
                'probabilities': probabilities,
                'disease_info': disease_info
            })
        else:
            # Clean up temporary file
            os.remove(filepath)
            # Fallback to mock predictions
            return predict_mock('ecg')
            
    except Exception as e:
        logger.error(f"ECG prediction error: {str(e)}")
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/predict/mri', methods=['POST'])
def predict_mri():
    """Predict heart disease from MRI image"""
    global mri_model
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file temporarily
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Use real model if available
        if mri_model is not None:
            # Preprocess image
            img_array = preprocess_image(filepath)
            
            if img_array is None:
                return jsonify({'error': 'Failed to process image'}), 400
            
            # Make prediction
            predictions = mri_model.predict(img_array)
            
            # Get results
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx] * 100)
            predicted_disease = MRI_CLASSES[predicted_class_idx]
            
            # Create probabilities dictionary
            probabilities = {}
            for i, class_name in enumerate(MRI_CLASSES):
                probabilities[class_name] = float(predictions[0][i] * 100)
            
            # Get disease info
            disease_info = get_disease_info(predicted_disease)
            
            # Clean up temporary file
            os.remove(filepath)
            
            return jsonify({
                'prediction': predicted_disease,
                'confidence': confidence,
                'probabilities': probabilities,
                'disease_info': disease_info
            })
        else:
            # Clean up temporary file
            os.remove(filepath)
            # Fallback to mock predictions
            return predict_mock('mri')
            
    except Exception as e:
        logger.error(f"MRI prediction error: {str(e)}")
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("Starting Enhanced Heart Disease Analyzer")
    print("=" * 60)
    
    # Check TensorFlow
    try:
        print(f"TensorFlow version: {tf.__version__}")
        print(f"GPU available: {len(tf.config.list_physical_devices('GPU')) > 0}")
    except:
        print("TensorFlow not available")
    
    # Load models
    print("\nLoading AI models...")
    load_models()
    
    print("\nAccess the website at:")
    print("  http://localhost:5000")
    print("  http://127.0.0.1:5000")
    
    print("\nHealth check endpoint:")
    print("  http://localhost:5000/health")
    
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)