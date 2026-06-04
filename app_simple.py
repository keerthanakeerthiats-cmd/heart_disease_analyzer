from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import numpy as np
import random
import json

app = Flask(__name__, static_folder='static')
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
MODEL_FOLDER = 'models'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODEL_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

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

def simulate_prediction(image_type):
    """Simulate a prediction for testing purposes"""
    classes = ECG_CLASSES if image_type == 'ecg' else MRI_CLASSES
    predicted_class = random.choice(classes)
    confidence = random.uniform(70, 99)
    
    # Build probabilities dictionary
    probabilities = {}
    remaining_prob = 100 - confidence
    other_classes = [cls for cls in classes if cls != predicted_class]
    
    # Assign confidence to predicted class
    probabilities[predicted_class] = round(confidence, 2)
    
    # Distribute remaining probability among other classes
    for i, class_name in enumerate(other_classes):
        if i == len(other_classes) - 1:
            # Last class gets remaining probability
            probabilities[class_name] = round(remaining_prob, 2)
        else:
            # Distribute some of the remaining probability
            prob = random.uniform(0, remaining_prob)
            probabilities[class_name] = round(prob, 2)
            remaining_prob -= prob
    
    # Adjust for rounding errors
    total = sum(probabilities.values())
    if abs(total - 100) > 0.01:
        # Adjust the highest probability class
        max_class = max(probabilities, key=probabilities.get)
        probabilities[max_class] += round(100 - total, 2)
    
    # Get detailed information
    warnings = get_detailed_warnings(predicted_class)
    dos_donts = get_dos_and_donts(predicted_class)
    
    result = {
        'prediction': predicted_class,
        'confidence': round(confidence, 2),
        'probabilities': probabilities,
        'recommendation': get_ecg_recommendation(predicted_class, confidence) if image_type == 'ecg' else get_mri_recommendation(predicted_class, confidence),
        'disease_info': get_disease_info(predicted_class),
        'warnings': warnings,
        'dos': dos_donts['dos'],
        'donts': dos_donts['donts']
    }
    
    return result

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

@app.route('/predict/ecg', methods=['POST'])
def predict_ecg():
    """Predict heart disease from ECG image"""
    try:
        # Simulate processing time
        import time
        time.sleep(2)
        
        # Simulate prediction
        result = simulate_prediction('ecg')
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in ECG prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/predict/mri', methods=['POST'])
def predict_mri():
    """Predict heart disease from MRI image"""
    try:
        # Simulate processing time
        import time
        time.sleep(2)
        
        # Simulate prediction
        result = simulate_prediction('mri')
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in MRI prediction: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/heart.jpg')
def heart_image():
    """Serve the heart image"""
    return send_from_directory('.', 'heart.jpg')

if __name__ == '__main__':
    print("Starting Heart Disease Analyzer (Simple Version)...")
    app.run(debug=True, host='0.0.0.0', port=5000)