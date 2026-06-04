# Quick Start Guide - Heart Disease Analyzer

## 🚀 Getting Started

### Prerequisites
- Python 3.8 - 3.11 (Python 3.13 may have TensorFlow compatibility issues)
- Windows/Linux/macOS
- 2GB+ free disk space

### Installation Steps

#### Option 1: Automatic Setup (Windows)
1. Double-click `setup.bat`
2. Wait for installation to complete
3. Sample images will be generated automatically

#### Option 2: Manual Setup
1. Open terminal/command prompt
2. Navigate to project directory:
   ```bash
   cd "c:\Users\VARUN COMPUTERS\Desktop\7th SEM\hhhhpppff"
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create sample test images:
   ```bash
   python create_samples.py
   ```

### Running the Application

#### Option 1: Using Start Script (Windows)
- Double-click `start.bat`

#### Option 2: Manual Start
```bash
python app.py
```

The server will start at: **http://localhost:5000**

### Using the Website

1. **Open your browser** and go to `http://localhost:5000`

2. **Upload ECG Image**:
   - Click on the left card "ECG Analysis"
   - Drag & drop or click to browse for an ECG image
   - Click "Analyze ECG" button
   - View results with confidence levels

3. **Upload MRI Image**:
   - Click on the right card "MRI Analysis"
   - Drag & drop or click to browse for an MRI image
   - Click "Analyze MRI" button
   - View detailed analysis results

### Sample Images
Sample test images are available in the `sample_images/` folder:
- `ecg_normal_1.png`, `ecg_normal_2.png` - Normal ECG samples
- `ecg_abnormal_1.png`, `ecg_abnormal_2.png` - Abnormal ECG samples
- `mri_normal_1.png`, `mri_normal_2.png` - Normal MRI samples
- `mri_disease_1.png`, `mri_disease_2.png` - Disease MRI samples

### Training Your Own Models

1. Organize your dataset:
   ```
   datasets/
     ecg/
       train/
         normal/     (place normal ECG images)
         abnormal/   (place abnormal ECG images)
       val/
         normal/
         abnormal/
     mri/
       train/
         normal/     (place normal MRI images)
         disease/    (place disease MRI images)
       val/
         normal/
         disease/
   ```

2. Run training script:
   ```bash
   python train_models.py
   ```

3. Trained models will be saved in `models/` folder

### Features Overview

✅ **Dual Analysis**: Both ECG and MRI scan analysis
✅ **AI-Powered**: Deep learning CNN models
✅ **Image Processing**: CLAHE, denoising, edge enhancement
✅ **Beautiful UI**: Animated gradient background
✅ **Real-time Results**: Instant predictions with confidence levels
✅ **Recommendations**: Medical recommendations based on analysis

### Troubleshooting

#### TensorFlow Installation Issues
If you're using Python 3.13, TensorFlow may not be compatible. Solutions:
1. Use Python 3.8-3.11
2. Or use conda environment:
   ```bash
   conda create -n heartdisease python=3.11
   conda activate heartdisease
   pip install -r requirements.txt
   ```

#### Module Not Found Errors
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Project Structure
```
hhhhpppff/
│
├── app.py                  # Main Flask application
├── train_models.py         # Model training script
├── create_samples.py       # Generate sample images
├── requirements.txt        # Python dependencies
├── setup.bat              # Windows setup script
├── start.bat              # Windows start script
│
├── templates/
│   └── index.html         # Main website
│
├── models/                # Trained models (after training)
│   ├── ecg_model.h5
│   └── mri_model.h5
│
├── sample_images/         # Sample test images
│   ├── ecg_normal_1.png
│   ├── ecg_abnormal_1.png
│   ├── mri_normal_1.png
│   └── mri_disease_1.png
│
├── datasets/             # Training datasets (you provide)
│   ├── ecg/
│   └── mri/
│
└── uploads/              # Temporary upload folder
```

### Important Notes

⚠️ **Medical Disclaimer**: This application is for educational and research purposes only. It is NOT a medical diagnostic tool and should NOT be used for actual medical diagnosis or treatment decisions. Always consult with qualified healthcare professionals.

⚠️ **Model Training**: The initial models are untrained. For production use, train them with real medical datasets.

### Support & Resources

- **Dataset Sources**:
  - ECG: MIT-BIH Arrhythmia Database, PTB Diagnostic ECG Database
  - MRI: Cardiac Atlas Project, UK Biobank (with proper permissions)

- **Documentation**: See README.md for detailed information

### Performance Tips

1. **GPU Acceleration**: Install TensorFlow-GPU for faster predictions
2. **Image Quality**: Use high-resolution medical images for better accuracy
3. **Browser**: Use modern browsers (Chrome, Firefox, Edge) for best UI experience

---

**Built with ❤️ using Flask, TensorFlow, and modern web technologies**
