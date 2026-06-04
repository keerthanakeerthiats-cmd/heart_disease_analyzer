from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

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
    """Mock ECG prediction (no AI needed for testing)"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Mock result for testing - more realistic
        import random
        diseases = ['Normal', 'Myocardial Infarction', 'Abnormal Heartbeat', 'History of MI', 'Arrhythmia']
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
        disease_info_map = {
            'Normal': {'description': 'No cardiac abnormalities detected.', 'severity': 'None', 'color': '#4ecdc4'},
            'Myocardial Infarction': {'description': 'Heart attack - occurs when blood flow to the heart muscle is blocked.', 'severity': 'Critical', 'color': '#ff0000'},
            'Abnormal Heartbeat': {'description': 'Irregular heart rhythm that may require monitoring.', 'severity': 'Moderate', 'color': '#ffa500'},
            'History of MI': {'description': 'Previous heart attack with possible residual effects.', 'severity': 'Moderate', 'color': '#ff6b6b'},
            'Arrhythmia': {'description': 'Abnormal heart rhythm requiring cardiac evaluation.', 'severity': 'Moderate', 'color': '#ffa500'}
        }
        
        disease_info = disease_info_map.get(predicted_disease, disease_info_map['Normal'])
        
        # Recommendation based on disease
        recommendations = {
            'Normal': 'Your ECG appears normal. Continue maintaining a healthy lifestyle with regular check-ups.',
            'Myocardial Infarction': '⚠️ URGENT: Signs of Myocardial Infarction detected. Seek immediate medical attention!',
            'Abnormal Heartbeat': 'Abnormal heartbeat pattern detected. We recommend professional cardiac evaluation.',
            'History of MI': 'Signs indicate a history of Myocardial Infarction. Please consult your cardiologist for proper management.',
            'Arrhythmia': 'Abnormal heart rhythm detected. Schedule an appointment with a cardiologist for evaluation.'
        }
        
        recommendation = recommendations.get(predicted_disease, 'Website is working! Install TensorFlow for real predictions.')
        
        result = {
            'prediction': predicted_disease,
            'confidence': confidence,
            'probabilities': probabilities,
            'recommendation': recommendation,
            'disease_info': disease_info,
            'warnings': [
                "Continue regular cardiac screenings as recommended by your physician",
                "Monitor for any unusual symptoms such as chest pain, shortness of breath, or palpitations",
                "Maintain a heart-healthy lifestyle with regular exercise and balanced nutrition"
            ],
            'dos': [
                "Engage in regular moderate-intensity exercise (150 minutes per week)",
                "Maintain a heart-healthy diet rich in fruits, vegetables, and whole grains",
                "Manage stress through relaxation techniques or meditation",
                "Get adequate sleep (7-9 hours per night)",
                "Stay hydrated and limit alcohol consumption"
            ],
            'donts': [
                "Do not smoke or use tobacco products",
                "Avoid excessive consumption of processed foods and trans fats",
                "Do not ignore symptoms like chest pain, dizziness, or irregular heartbeat",
                "Avoid extreme physical exertion without proper conditioning",
                "Do not skip regular medical check-ups"
            ]
        }
        
        return jsonify(result)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/predict/mri', methods=['POST'])
def predict_mri():
    """Mock MRI prediction (no AI needed for testing)"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Mock result for testing - more realistic
        import random
        diseases = ['Normal', 'Cardiomyopathy', 'Coronary Artery Disease', 'Heart Failure', 'Myocardial Infarction']
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
        disease_info_map = {
            'Normal': {'description': 'No cardiac abnormalities detected.', 'severity': 'None', 'color': '#4ecdc4'},
            'Cardiomyopathy': {'description': 'Disease of the heart muscle affecting pumping ability.', 'severity': 'High', 'color': '#ff6b6b'},
            'Coronary Artery Disease': {'description': 'Narrowing of coronary arteries reducing blood flow to heart.', 'severity': 'High', 'color': '#ff4444'},
            'Heart Failure': {'description': 'Condition where heart cannot pump blood effectively.', 'severity': 'Critical', 'color': '#ff0000'},
            'Myocardial Infarction': {'description': 'Heart attack - occurs when blood flow to the heart muscle is blocked.', 'severity': 'Critical', 'color': '#ff0000'}
        }
        
        disease_info = disease_info_map.get(predicted_disease, disease_info_map['Normal'])
        
        # Recommendation based on disease
        recommendations = {
            'Normal': 'Your cardiac MRI appears normal. Maintain regular check-ups and healthy lifestyle.',
            'Cardiomyopathy': 'Signs of Cardiomyopathy detected. Consult a cardiologist for proper diagnosis and treatment plan.',
            'Coronary Artery Disease': 'Indicators of Coronary Artery Disease found. Immediate consultation with a cardiologist is recommended.',
            'Heart Failure': '⚠️ Signs of Heart Failure detected. Please seek urgent medical attention for proper management.',
            'Myocardial Infarction': '⚠️ CRITICAL: Signs of Myocardial Infarction detected. Seek immediate emergency medical care!'
        }
        
        recommendation = recommendations.get(predicted_disease, 'Website is working! Install TensorFlow for real predictions.')
        
        result = {
            'prediction': predicted_disease,
            'confidence': confidence,
            'probabilities': probabilities,
            'recommendation': recommendation,
            'disease_info': disease_info,
            'warnings': [
                "Continue regular cardiac screenings as recommended by your physician",
                "Monitor for any unusual symptoms such as chest pain, shortness of breath, or palpitations",
                "Maintain a heart-healthy lifestyle with regular exercise and balanced nutrition"
            ],
            'dos': [
                "Engage in regular moderate-intensity exercise (150 minutes per week)",
                "Maintain a heart-healthy diet rich in fruits, vegetables, and whole grains",
                "Manage stress through relaxation techniques or meditation",
                "Get adequate sleep (7-9 hours per night)",
                "Stay hydrated and limit alcohol consumption"
            ],
            'donts': [
                "Do not smoke or use tobacco products",
                "Avoid excessive consumption of processed foods and trans fats",
                "Do not ignore symptoms like chest pain, dizziness, or irregular heartbeat",
                "Avoid extreme physical exertion without proper conditioning",
                "Do not skip regular medical check-ups"
            ]
        }
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("Starting Heart Disease Analyzer (Test Mode)")
    print("=" * 60)
    print("\n✓ Server running without TensorFlow")
    print("✓ Website will work but predictions are mock/test data")
    print("✓ Install TensorFlow later for real AI predictions")
    print("\nOpen browser to: http://localhost:5000")
    print("\nPress Ctrl+C to stop")
    print("=" * 60)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
