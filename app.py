from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import numpy as np
from PIL import Image
import cv2
import tensorflow as tf
try:
    from tensorflow import keras
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
    from tensorflow.keras.preprocessing.image import img_to_array
except ImportError:
    import keras
    from keras.models import Sequential
    from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
    from keras.preprocessing.image import img_to_array
import io
import base64

# Import advanced modules
from advanced_image_preprocessing import AdvancedImageProcessor
from model_ensemble import create_optimized_ensemble, load_ensemble_class_names

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
MODEL_FOLDER = 'models'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODEL_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


def load_model_safe(model_path):
    """Safely load a model with compatibility for different TF/Keras versions"""
    try:
        # Try TensorFlow Keras first
        from tensorflow.keras.models import load_model
        return load_model(model_path)
    except ImportError:
        # Fallback to older Keras
        try:
            from keras.models import load_model
            return load_model(model_path)
        except ImportError:
            # If neither works, return None
            return None


def create_model_safe(model_fn, *args, **kwargs):
    """Safely create a model with compatibility for different TF/Keras versions"""
    try:
        return model_fn(*args, **kwargs)
    except Exception:
        # Fallback for older versions
        try:
            # Re-import to ensure availability
            import tensorflow as tf
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
            return model_fn(*args, **kwargs)
        except ImportError:
            import keras
            from keras.models import Sequential
            from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
            return model_fn(*args, **kwargs)


# Global variables for models
ecg_model = None
mri_model = None

# Initialize advanced processor
processor = AdvancedImageProcessor()

# Try to initialize ensemble models
ecg_ensemble = None
mri_ensemble = None

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

def create_ecg_model(num_classes=5):
    """Create CNN model for ECG image classification"""
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        
        Conv2D(64, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        
        Conv2D(128, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        
        Conv2D(256, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(256, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')  # Multi-class: 5 disease types
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def create_mri_model(num_classes=5):
    """Create CNN model for MRI image classification"""
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        
        Conv2D(64, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        
        Conv2D(128, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        
        Conv2D(256, (3, 3), activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(256, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')  # Multi-class: 5 disease types
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def preprocess_image(image_file, target_size=(128, 128)):
    """Preprocess uploaded image for model prediction"""
    try:
        # Read image
        image = Image.open(image_file)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image
        image = image.resize(target_size)
        
        # Convert to array and normalize
        img_array = img_to_array(image)
        img_array = img_array / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    except Exception as e:
        print(f"Error preprocessing image: {str(e)}")
        return None

def enhance_ecg_image(image_array):
    """Apply advanced image processing techniques to enhance ECG images"""
    try:
        # Use the advanced processor
        enhanced = processor.enhance_ecg_image(image_array)
        return enhanced
    except Exception as e:
        print(f"Error enhancing ECG image: {str(e)}")
        # Fall back to original method if advanced method fails
        img = (image_array[0] * 255).astype(np.uint8)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)
        enhanced_rgb = cv2.cvtColor(denoised, cv2.COLOR_GRAY2RGB)
        enhanced_rgb = enhanced_rgb / 255.0
        enhanced_rgb = np.expand_dims(enhanced_rgb, axis=0)
        return enhanced_rgb

def enhance_mri_image(image_array):
    """Apply advanced image processing techniques to enhance MRI images"""
    try:
        # Use the advanced processor
        enhanced = processor.enhance_mri_image(image_array)
        return enhanced
    except Exception as e:
        print(f"Error enhancing MRI image: {str(e)}")
        # Fall back to original method if advanced method fails
        img = (image_array[0] * 255).astype(np.uint8)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        blurred = cv2.GaussianBlur(enhanced, (5, 5), 0)
        gaussian = cv2.GaussianBlur(blurred, (9, 9), 10.0)
        unsharp = cv2.addWeighted(blurred, 1.5, gaussian, -0.5, 0)
        enhanced_rgb = cv2.cvtColor(unsharp, cv2.COLOR_GRAY2RGB)
        enhanced_rgb = enhanced_rgb / 255.0
        enhanced_rgb = np.expand_dims(enhanced_rgb, axis=0)
        return enhanced_rgb

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/results')
def results():
    """Render the results page"""
    return render_template('results.html')

@app.route('/accuracy')
def accuracy():
    """Render the accuracy visualization page"""
    return render_template('accuracy.html')

@app.route('/heart.jpg')
def heart_image():
    """Serve the heart image"""
    return send_from_directory('.', 'heart.jpg')

@app.route('/predict/ecg', methods=['POST'])
def predict_ecg():
    """Predict heart disease from ECG image"""
    global ecg_model, ecg_ensemble
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Preprocess image
        img_array = preprocess_image(file)
        
        if img_array is None:
            return jsonify({'error': 'Failed to process image'}), 400
        
        # Enhance ECG image with advanced techniques
        enhanced_img = enhance_ecg_image(img_array)
        
        # Try to use ensemble if available, otherwise use regular model
        prediction = None
        predicted_class_idx = None
        confidence = None
        predicted_class = None
        probabilities = {}
        
        # Try to initialize ensemble if not already done
        if ecg_ensemble is None:
            ecg_ensemble = create_optimized_ensemble('ecg')
        
        if ecg_ensemble is not None and len(ecg_ensemble.models) > 0:
            # Use ensemble prediction
            ensemble_result = ecg_ensemble.predict_with_confidence(enhanced_img)
            prediction = ensemble_result['ensemble_prediction']
            confidence = ensemble_result['confidence']
        else:
            # Initialize model if not loaded
            if ecg_model is None:
                # Try to load enhanced model first
                enhanced_model_path = os.path.join(MODEL_FOLDER, 'enhanced_ecg_model.h5')
                standard_model_path = os.path.join(MODEL_FOLDER, 'ecg_model.h5')
                best_model_path = os.path.join(MODEL_FOLDER, 'best_ecg_model.h5')
                advanced_model_path = os.path.join(MODEL_FOLDER, 'advanced_ecg_model.h5')
                
                if os.path.exists(advanced_model_path):
                    # Load advanced model if available
                    ecg_model = load_model_safe(advanced_model_path)
                    if ecg_model is not None:
                        print(f"Loaded advanced ECG model from: {advanced_model_path}")
                    else:
                        print(f"Failed to load advanced ECG model from: {advanced_model_path}, creating new model")
                        ecg_model = create_model_safe(create_ecg_model, num_classes=len(ECG_CLASSES))
                elif os.path.exists(best_model_path):
                    # Load best model if available
                    ecg_model = create_model_safe(create_ecg_model, num_classes=len(ECG_CLASSES))
                    ecg_model.load_weights(best_model_path)
                    print(f"Loaded enhanced ECG model from: {best_model_path}")
                elif os.path.exists(enhanced_model_path):
                    # Load enhanced model if available
                    ecg_model = create_model_safe(create_ecg_model, num_classes=len(ECG_CLASSES))
                    ecg_model.load_weights(enhanced_model_path)
                    print(f"Loaded enhanced ECG model from: {enhanced_model_path}")
                elif os.path.exists(standard_model_path):
                    # Load standard model if available
                    ecg_model = create_model_safe(create_ecg_model, num_classes=len(ECG_CLASSES))
                    ecg_model.load_weights(standard_model_path)
                    print(f"Loaded standard ECG model from: {standard_model_path}")
                else:
                    # Create new model if none exists
                    ecg_model = create_model_safe(create_ecg_model, num_classes=len(ECG_CLASSES))
                    print("Created new ECG model")
            
            # Make prediction with single model
            prediction = ecg_model.predict(enhanced_img)
            predicted_class_idx = np.argmax(prediction[0])
            predicted_class = ECG_CLASSES[predicted_class_idx]
            confidence = float(np.max(prediction[0]) * 100)
        
        # Handle prediction based on whether ensemble was used
        if ecg_ensemble is not None and len(ecg_ensemble.models) > 0:
            predicted_class_idx = np.argmax(prediction[0])
            predicted_class = ECG_CLASSES[predicted_class_idx]
            
            # Calculate probabilities from ensemble prediction
            for idx, class_name in enumerate(ECG_CLASSES):
                probabilities[class_name] = round(float(prediction[0][idx] * 100), 2)
        else:
            # Use single model probabilities
            for idx, class_name in enumerate(ECG_CLASSES):
                probabilities[class_name] = round(float(prediction[0][idx] * 100), 2)
        
        # Get class names dynamically if available
        try:
            dynamic_classes = load_ensemble_class_names('ecg')
            if len(dynamic_classes) > 0:
                ECG_CLASSES_DYNAMIC = dynamic_classes
                predicted_class = ECG_CLASSES_DYNAMIC[predicted_class_idx]
                
                # Update probabilities with dynamic classes
                probabilities = {}
                for idx, class_name in enumerate(ECG_CLASSES_DYNAMIC):
                    probabilities[class_name] = round(float(prediction[0][idx] * 100), 2)
        except:
            pass  # Use default classes if dynamic loading fails
        
        # Detailed analysis
        warnings = get_detailed_warnings(predicted_class)
        dos_donts = get_dos_and_donts(predicted_class)
        
        result = {
            'prediction': predicted_class,
            'confidence': round(confidence, 2),
            'probabilities': probabilities,
            'recommendation': get_ecg_recommendation(predicted_class, confidence),
            'disease_info': get_disease_info(predicted_class),
            'warnings': warnings,
            'dos': dos_donts['dos'],
            'donts': dos_donts['donts']
        }
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in ECG prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/predict/mri', methods=['POST'])
def predict_mri():
    """Predict heart disease from MRI image"""
    global mri_model, mri_ensemble
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Preprocess image
        img_array = preprocess_image(file)
        
        if img_array is None:
            return jsonify({'error': 'Failed to process image'}), 400
        
        # Enhance MRI image with advanced techniques
        enhanced_img = enhance_mri_image(img_array)
        
        # Try to use ensemble if available, otherwise use regular model
        prediction = None
        predicted_class_idx = None
        confidence = None
        predicted_class = None
        probabilities = {}
        
        # Try to initialize ensemble if not already done
        if mri_ensemble is None:
            mri_ensemble = create_optimized_ensemble('mri')
        
        if mri_ensemble is not None and len(mri_ensemble.models) > 0:
            # Use ensemble prediction
            ensemble_result = mri_ensemble.predict_with_confidence(enhanced_img)
            prediction = ensemble_result['ensemble_prediction']
            confidence = ensemble_result['confidence']
        else:
            # Initialize model if not loaded
            if mri_model is None:
                # Try to load enhanced model first
                enhanced_model_path = os.path.join(MODEL_FOLDER, 'enhanced_mri_model.h5')
                standard_model_path = os.path.join(MODEL_FOLDER, 'mri_model.h5')
                best_model_path = os.path.join(MODEL_FOLDER, 'best_mri_model.h5')
                advanced_model_path = os.path.join(MODEL_FOLDER, 'advanced_mri_model.h5')
                
                if os.path.exists(advanced_model_path):
                    # Load advanced model if available
                    mri_model = load_model_safe(advanced_model_path)
                    if mri_model is not None:
                        print(f"Loaded advanced MRI model from: {advanced_model_path}")
                    else:
                        print(f"Failed to load advanced MRI model from: {advanced_model_path}, creating new model")
                        mri_model = create_model_safe(create_mri_model, num_classes=len(MRI_CLASSES))
                elif os.path.exists(best_model_path):
                    # Load best model if available
                    mri_model = create_model_safe(create_mri_model, num_classes=len(MRI_CLASSES))
                    mri_model.load_weights(best_model_path)
                    print(f"Loaded enhanced MRI model from: {best_model_path}")
                elif os.path.exists(enhanced_model_path):
                    # Load enhanced model if available
                    mri_model = create_model_safe(create_mri_model, num_classes=len(MRI_CLASSES))
                    mri_model.load_weights(enhanced_model_path)
                    print(f"Loaded enhanced MRI model from: {enhanced_model_path}")
                elif os.path.exists(standard_model_path):
                    # Load standard model if available
                    mri_model = create_model_safe(create_mri_model, num_classes=len(MRI_CLASSES))
                    mri_model.load_weights(standard_model_path)
                    print(f"Loaded standard MRI model from: {standard_model_path}")
                else:
                    # Create new model if none exists
                    mri_model = create_model_safe(create_mri_model, num_classes=len(MRI_CLASSES))
                    print("Created new MRI model")
            
            # Make prediction with single model
            prediction = mri_model.predict(enhanced_img)
            predicted_class_idx = np.argmax(prediction[0])
            predicted_class = MRI_CLASSES[predicted_class_idx]
            confidence = float(np.max(prediction[0]) * 100)
        
        # Handle prediction based on whether ensemble was used
        if mri_ensemble is not None and len(mri_ensemble.models) > 0:
            predicted_class_idx = np.argmax(prediction[0])
            predicted_class = MRI_CLASSES[predicted_class_idx]
            
            # Calculate probabilities from ensemble prediction
            for idx, class_name in enumerate(MRI_CLASSES):
                probabilities[class_name] = round(float(prediction[0][idx] * 100), 2)
        else:
            # Use single model probabilities
            for idx, class_name in enumerate(MRI_CLASSES):
                probabilities[class_name] = round(float(prediction[0][idx] * 100), 2)
        
        # Get class names dynamically if available
        try:
            dynamic_classes = load_ensemble_class_names('mri')
            if len(dynamic_classes) > 0:
                MRI_CLASSES_DYNAMIC = dynamic_classes
                predicted_class = MRI_CLASSES_DYNAMIC[predicted_class_idx]
                
                # Update probabilities with dynamic classes
                probabilities = {}
                for idx, class_name in enumerate(MRI_CLASSES_DYNAMIC):
                    probabilities[class_name] = round(float(prediction[0][idx] * 100), 2)
        except:
            pass  # Use default classes if dynamic loading fails
        
        # Detailed analysis
        warnings = get_detailed_warnings(predicted_class)
        dos_donts = get_dos_and_donts(predicted_class)
        
        result = {
            'prediction': predicted_class,
            'confidence': round(confidence, 2),
            'probabilities': probabilities,
            'recommendation': get_mri_recommendation(predicted_class, confidence),
            'disease_info': get_disease_info(predicted_class),
            'warnings': warnings,
            'dos': dos_donts['dos'],
            'donts': dos_donts['donts']
        }
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in MRI prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

def get_ecg_recommendation(predicted_class, confidence):
    """Generate recommendation based on ECG prediction"""
    if predicted_class == 'Normal':
        if confidence > 90:
            return "Your ECG appears normal. Continue maintaining a healthy lifestyle with regular check-ups."
        else:
            return "Your ECG appears normal, but please consult a cardiologist for confirmation."
    elif predicted_class == 'Myocardial Infarction':
        return "⚠️ URGENT: Signs of Myocardial Infarction detected. Seek immediate medical attention!"
    elif predicted_class == 'History of MI':
        return "Signs indicate a history of Myocardial Infarction. Please consult your cardiologist for proper management."
    elif predicted_class == 'Arrhythmia':
        return "Abnormal heart rhythm detected. Schedule an appointment with a cardiologist for evaluation."
    else:  # Abnormal Heartbeat
        return "Abnormal heartbeat pattern detected. We recommend professional cardiac evaluation."

def get_mri_recommendation(predicted_class, confidence):
    """Generate recommendation based on MRI prediction"""
    if predicted_class == 'Normal':
        if confidence > 90:
            return "Your cardiac MRI appears normal. Maintain regular check-ups and healthy lifestyle."
        else:
            return "Your cardiac MRI appears normal, but please consult a cardiologist for detailed analysis."
    elif predicted_class == 'Cardiomyopathy':
        return "Signs of Cardiomyopathy detected. Consult a cardiologist for proper diagnosis and treatment plan."
    elif predicted_class == 'Coronary Artery Disease':
        return "Indicators of Coronary Artery Disease found. Immediate consultation with a cardiologist is recommended."
    elif predicted_class == 'Heart Failure':
        return "⚠️ Signs of Heart Failure detected. Please seek urgent medical attention for proper management."
    else:  # Myocardial Infarction
        return "⚠️ CRITICAL: Signs of Myocardial Infarction detected. Seek immediate emergency medical care!"

def get_detailed_warnings(predicted_class):
    """Get detailed warnings based on the predicted class"""
    warnings = {
        'Normal': [
            "Continue regular cardiac screenings as recommended by your physician",
            "Monitor for any unusual symptoms such as chest pain, shortness of breath, or palpitations",
            "Maintain a heart-healthy lifestyle with regular exercise and balanced nutrition"
        ],
        'Myocardial Infarction': [
            "⚠️ IMMEDIATE MEDICAL ATTENTION REQUIRED",
            "Do not delay in seeking emergency medical care",
            "Avoid physical exertion until evaluated by a physician",
            "Take prescribed medications as directed"
        ],
        'History of MI': [
            "Follow your cardiologist's treatment plan closely",
            "Take prescribed medications regularly",
            "Avoid strenuous activities without medical clearance",
            "Report any new or worsening symptoms immediately"
        ],
        'Arrhythmia': [
            "Monitor your pulse regularly",
            "Avoid stimulants like caffeine and nicotine",
            "Take prescribed antiarrhythmic medications as directed",
            "Report episodes of rapid or irregular heartbeat"
        ],
        'Abnormal Heartbeat': [
            "Avoid triggers that may worsen symptoms",
            "Limit caffeine and alcohol intake",
            "Maintain regular follow-up appointments with your cardiologist",
            "Report any fainting episodes or severe dizziness"
        ],
        'Cardiomyopathy': [
            "Restrict sodium intake to reduce fluid retention",
            "Monitor weight daily for signs of fluid retention",
            "Take prescribed medications exactly as directed",
            "Avoid alcohol completely"
        ],
        'Coronary Artery Disease': [
            "Follow a low-fat, low-sodium diet",
            "Take prescribed medications including aspirin and statins",
            "Participate in a supervised cardiac rehabilitation program",
            "Stop smoking immediately if you smoke"
        ],
        'Heart Failure': [
            "Monitor daily weight and report sudden increases",
            "Limit fluid intake as prescribed",
            "Weigh yourself daily at the same time",
            "Take diuretics and other medications as prescribed"
        ]
    }
    return warnings.get(predicted_class, [
        "Follow up with your healthcare provider for proper evaluation",
        "Monitor for any changes in symptoms",
        "Maintain a heart-healthy lifestyle"
    ])

def get_dos_and_donts(predicted_class):
    """Get dos and don'ts based on the predicted class"""
    dos = {
        'Normal': [
            "Engage in regular moderate-intensity exercise (150 minutes per week)",
            "Maintain a heart-healthy diet rich in fruits, vegetables, and whole grains",
            "Manage stress through relaxation techniques or meditation",
            "Get adequate sleep (7-9 hours per night)",
            "Stay hydrated and limit alcohol consumption"
        ],
        'Myocardial Infarction': [
            "Seek immediate emergency medical attention",
            "Take aspirin if prescribed and not allergic",
            "Remain calm and rest while awaiting medical help",
            "Have someone stay with you until help arrives"
        ],
        'History of MI': [
            "Take prescribed medications regularly",
            "Attend cardiac rehabilitation sessions",
            "Follow a heart-healthy diet",
            "Exercise as recommended by your healthcare provider"
        ],
        'Arrhythmia': [
            "Practice stress-reduction techniques",
            "Maintain a consistent sleep schedule",
            "Stay hydrated",
            "Follow up regularly with your cardiologist"
        ],
        'Abnormal Heartbeat': [
            "Practice deep breathing exercises",
            "Maintain a healthy weight",
            "Stay hydrated",
            "Get regular medical check-ups"
        ],
        'Cardiomyopathy': [
            "Follow a low-sodium diet",
            "Take medications as prescribed",
            "Monitor symptoms daily",
            "Attend all medical appointments"
        ],
        'Coronary Artery Disease': [
            "Exercise regularly as prescribed",
            "Eat a Mediterranean-style diet",
            "Take medications as directed",
            "Manage stress effectively"
        ],
        'Heart Failure': [
            "Monitor weight daily",
            "Limit sodium intake",
            "Take medications as prescribed",
            "Follow fluid restrictions if advised"
        ]
    }
    
    donts = {
        'Normal': [
            "Do not smoke or use tobacco products",
            "Avoid excessive consumption of processed foods and trans fats",
            "Do not ignore symptoms like chest pain, dizziness, or irregular heartbeat",
            "Avoid extreme physical exertion without proper conditioning",
            "Do not skip regular medical check-ups"
        ],
        'Myocardial Infarction': [
            "Do not drive yourself to the hospital",
            "Do not eat or drink anything",
            "Do not take any medications except those prescribed",
            "Do not ignore symptoms even if they seem mild"
        ],
        'History of MI': [
            "Do not stop taking prescribed medications without consulting your doctor",
            "Avoid heavy lifting or strenuous activities without approval",
            "Do not smoke or expose yourself to secondhand smoke",
            "Do not skip cardiac rehabilitation sessions"
        ],
        'Arrhythmia': [
            "Do not consume excessive caffeine or energy drinks",
            "Avoid over-the-counter cold medications without consulting your doctor",
            "Do not smoke or use recreational drugs",
            "Do not ignore skipped beats or palpitations"
        ],
        'Abnormal Heartbeat': [
            "Do not panic during episodes",
            "Avoid known triggers",
            "Do not self-medicate",
            "Do not ignore persistent symptoms"
        ],
        'Cardiomyopathy': [
            "Do not consume alcohol",
            "Avoid NSAIDs like ibuprofen unless approved by your doctor",
            "Do not skip medications",
            "Do not ignore weight gain or swelling"
        ],
        'Coronary Artery Disease': [
            "Do not smoke or use tobacco products",
            "Avoid saturated and trans fats",
            "Do not ignore chest pain or discomfort",
            "Do not skip prescribed medications"
        ],
        'Heart Failure': [
            "Do not add salt to food",
            "Avoid NSAIDs without medical approval",
            "Do not ignore sudden weight gain",
            "Do not skip medications or medical appointments"
        ]
    }
    
    return {
        'dos': dos.get(predicted_class, [
            "Follow your healthcare provider's recommendations",
            "Maintain a healthy lifestyle",
            "Take medications as prescribed",
            "Attend regular check-ups"
        ]),
        'donts': donts.get(predicted_class, [
            "Do not ignore symptoms",
            "Do not skip medications",
            "Do not engage in unsupervised strenuous activity",
            "Do not smoke or use tobacco products"
        ])
    }

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

if __name__ == '__main__':
    print("Starting Enhanced Heart Disease Analyzer...")
    print("Loading advanced models and preprocessing systems...")
    app.run(debug=True, host='0.0.0.0', port=5001)  # Changed to port 5001 as per memory