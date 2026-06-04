"""
Simple test app to verify the website is working correctly
"""

from flask import Flask, render_template, request, jsonify
import os
import random

app = Flask(__name__)

# Create uploads directory if it doesn't exist
os.makedirs('uploads', exist_ok=True)

# Sample disease classes
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

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/predict/<type>', methods=['POST'])
def predict(type):
    """Simple prediction endpoint that returns mock data"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save file temporarily
        filepath = os.path.join('uploads', file.filename)
        file.save(filepath)
        
        # Generate mock results
        if type == 'ecg':
            classes = ECG_CLASSES
        else:  # mri
            classes = MRI_CLASSES
        
        # Select random disease
        predicted_disease = random.choice(classes)
        
        # Generate realistic probabilities
        probabilities = {}
        total = 0
        for disease in classes:
            prob = random.uniform(5, 40) if disease != predicted_disease else random.uniform(60, 95)
            probabilities[disease] = round(prob, 1)
            total += prob
        
        # Normalize to 100%
        for disease in classes:
            probabilities[disease] = round(probabilities[disease] * 100 / total, 1)
        
        # Get predicted disease with highest probability
        predicted_disease = max(probabilities, key=probabilities.get)
        confidence = probabilities[predicted_disease]
        
        # Get disease info
        disease_info = get_disease_info(predicted_disease)
        
        # Create recommendation based on disease
        if predicted_disease == 'Normal':
            recommendation = "Your heart appears healthy. Continue maintaining a healthy lifestyle with regular check-ups."
        elif predicted_disease in ['Myocardial Infarction', 'Heart Failure']:
            recommendation = f"⚠️ CRITICAL: Signs of {predicted_disease} detected. Seek immediate medical attention!"
        else:
            recommendation = f"Signs of {predicted_disease} detected. Please consult a cardiologist for proper evaluation."
        
        # Clean up temporary file
        os.remove(filepath)
        
        # Return results
        return jsonify({
            'prediction': predicted_disease,
            'confidence': confidence,
            'probabilities': probabilities,
            'recommendation': recommendation,
            'disease_info': disease_info
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("Starting Simple Test Heart Disease Analyzer")
    print("=" * 60)
    print("Access the website at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)