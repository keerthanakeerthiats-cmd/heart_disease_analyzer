# Heart Disease Analyzer

AI-powered web application for detecting heart diseases using ECG and MRI image analysis.

## Features

- **ECG Analysis**: Upload ECG scans for automated heart rhythm analysis
- **MRI Analysis**: Upload cardiac MRI scans for structural heart disease detection
- **Real-time Processing**: Fast image analysis with immediate results
- **Beautiful UI**: Stunning animated gradient background with smooth interactions
- **Deep Learning**: CNN models for accurate image classification
- **Image Enhancement**: Advanced preprocessing techniques (CLAHE, denoising, edge enhancement)
- **Trained Models Support**: Use your own trained models for accurate predictions

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Option 1: Quick Start (Using Pre-trained Models)

1. Place your trained models in the `models` folder:
   - `models/ecg_model.h5` (for ECG predictions)
   - `models/mri_model.h5` (for MRI predictions)

2. Start the Flask server:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

### Option 2: Automated Start

Double-click `START_WITH_TRAINED_MODELS.bat` to automatically check for models and start the website.

## Usage

1. **Upload ECG Image**:
   - Click or drag-and-drop an ECG image into the left card
   - Click "Analyze ECG" button
   - View results with confidence levels and recommendations

2. **Upload MRI Image**:
   - Click or drag-and-drop an MRI image into the right card
   - Click "Analyze MRI" button
   - View results with detailed probabilities

## Training Your Own Models

### Automated Training

1. Double-click `TRAIN_REAL_AI.bat`
2. Wait 1-3 hours for training to complete
3. The website will automatically start with real AI predictions

### Manual Training

1. Prepare your dataset in the proper folder structure
2. Run the training script:
```bash
python train_real_models.py
```

## Model Information

The application uses Convolutional Neural Networks (CNN) for multi-class disease classification:

### ECG Model (5 Classes)
- Normal
- Myocardial Infarction (Heart Attack)
- Abnormal Heartbeat
- History of MI
- Arrhythmia (Irregular Rhythm)

### MRI Model (5 Classes)
- Normal
- Cardiomyopathy (Heart Muscle Disease)
- Coronary Artery Disease
- Heart Failure
- Myocardial Infarction

### Architecture
- 4 Convolutional blocks with BatchNormalization
- MaxPooling layers for dimensionality reduction
- Dropout layers for regularization (0.5, 0.3)
- Dense layers for classification
- Softmax activation for multi-class output

## Image Processing Techniques

- **CLAHE**: Contrast Limited Adaptive Histogram Equalization
- **Denoising**: Non-local means denoising
- **Edge Enhancement**: Unsharp masking
- **Normalization**: Pixel value scaling

## Technologies Used

- **Backend**: Flask, TensorFlow, Keras, OpenCV
- **Frontend**: HTML5, CSS3, JavaScript
- **ML Framework**: TensorFlow 2.15
- **Image Processing**: OpenCV, PIL

## Author
- Keerthana P T
- ECE Student

## Note

⚠️ **Important**: This application is for educational and screening purposes only. The models are initialized with random weights. For production use, you need to train the models on actual medical datasets.

To train the models:
1. Prepare labeled ECG and MRI datasets
2. Train the models using the provided architecture
3. Save the trained weights to the `models/` folder as `ecg_model.h5` and `mri_model.h5`

For detailed instructions on using trained models, see [USING_TRAINED_MODELS.md](USING_TRAINED_MODELS.md)

## Disclaimer

This tool is NOT a substitute for professional medical diagnosis. Always consult with qualified healthcare professionals for accurate diagnosis and treatment.
