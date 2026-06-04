# Kaggle Dataset Download and Training Guide

## 📊 Recommended Kaggle Datasets

### For ECG Analysis

#### 1. **PTB-XL ECG Dataset** (Recommended)
- **Link**: https://www.kaggle.com/datasets/khyeh0719/ptb-xl-dataset
- **Description**: Large publicly available ECG dataset with 21,837 records
- **Classes**: Multiple cardiac conditions including MI, arrhythmia, etc.
- **Format**: CSV + ECG signals

#### 2. **ECG Heartbeat Categorization Dataset**
- **Link**: https://www.kaggle.com/datasets/shayanfazeli/heartbeat
- **Description**: 109,446 ECG samples categorized into 5 classes
- **Classes**: 
  - Normal (N)
  - Supraventricular premature beat (S)
  - Premature ventricular contraction (V)
  - Fusion of ventricular and normal beat (F)
  - Unclassifiable beat (Q)
- **Format**: CSV files ready for training

#### 3. **MIT-BIH Arrhythmia Database**
- **Link**: https://www.kaggle.com/datasets/mondejar/mitbih-database
- **Description**: Classic ECG arrhythmia dataset
- **Classes**: 5 heartbeat types
- **Format**: CSV

### For MRI/Cardiac Image Analysis

#### 1. **Cardiac MRI Dataset** (Recommended)
- **Link**: https://www.kaggle.com/datasets/andrewmvd/cardiac-mri-classification
- **Description**: Cardiac MRI images with multiple views
- **Classes**: Normal and various cardiac conditions

#### 2. **Heart Disease Classification Dataset**
- **Link**: https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset
- **Description**: Clinical data for heart disease prediction
- **Note**: Can be combined with imaging data

## 🔧 Setup Kaggle API

### Step 1: Install Kaggle API
```bash
pip install kaggle
```

### Step 2: Get Kaggle API Credentials
1. Go to https://www.kaggle.com/
2. Click on your profile picture → Account
3. Scroll to "API" section
4. Click "Create New API Token"
5. Download `kaggle.json` file

### Step 3: Configure Kaggle API (Windows)
```powershell
# Create .kaggle directory
mkdir $env:USERPROFILE\.kaggle

# Move kaggle.json to .kaggle folder
move kaggle.json $env:USERPROFILE\.kaggle\

# Set permissions (for security)
icacls "$env:USERPROFILE\.kaggle\kaggle.json" /inheritance:r /grant:r "$($env:USERNAME):F"
```

## 📥 Download Datasets

### ECG Dataset Download Script
```python
# download_ecg_dataset.py
import kaggle
import os
import zipfile
import shutil

def download_ecg_dataset():
    """Download ECG Heartbeat Categorization Dataset"""
    print("Downloading ECG dataset from Kaggle...")
    
    # Download the dataset
    kaggle.api.dataset_download_files(
        'shayanfazeli/heartbeat',
        path='temp_ecg',
        unzip=True
    )
    
    print("Organizing ECG dataset...")
    # Organize into our folder structure
    # (You'll need to organize based on the dataset structure)
    
    print("ECG dataset ready!")

if __name__ == '__main__':
    download_ecg_dataset()
```

### Manual Download Instructions

1. **Visit the dataset page** on Kaggle
2. **Click "Download"** button
3. **Extract the zip file** to your project folder
4. **Organize files** according to our structure:

```
datasets/
  ecg/
    train/
      normal/
      myocardial_infarction/
      abnormal_heartbeat/
      history_of_mi/
      arrhythmia/
    val/
      normal/
      myocardial_infarction/
      abnormal_heartbeat/
      history_of_mi/
      arrhythmia/
  mri/
    train/
      normal/
      cardiomyopathy/
      coronary_artery_disease/
      heart_failure/
      myocardial_infarction/
    val/
      normal/
      cardiomyopathy/
      coronary_artery_disease/
      heart_failure/
      myocardial_infarction/
```

## 🚀 Automated Dataset Preparation Script

Save this as `prepare_kaggle_dataset.py`:

```python
"""
Automated script to download and prepare Kaggle datasets
"""
import os
import shutil
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

def prepare_ecg_heartbeat_dataset():
    """
    Prepare ECG Heartbeat Categorization Dataset
    Dataset: shayanfazeli/heartbeat
    """
    print("="*60)
    print("Preparing ECG Heartbeat Dataset")
    print("="*60)
    
    # Check if dataset files exist
    if not os.path.exists('temp_ecg/mitbih_train.csv'):
        print("Dataset not found. Please download manually from:")
        print("https://www.kaggle.com/datasets/shayanfazeli/heartbeat")
        return
    
    # Load the data
    train_df = pd.read_csv('temp_ecg/mitbih_train.csv', header=None)
    test_df = pd.read_csv('temp_ecg/mitbih_test.csv', header=None)
    
    # Combine train and test
    all_data = pd.concat([train_df, test_df], ignore_index=True)
    
    # Separate features and labels
    X = all_data.iloc[:, :-1].values
    y = all_data.iloc[:, -1].values
    
    # Class mapping (original dataset has 5 classes)
    class_mapping = {
        0: 'normal',
        1: 'abnormal_heartbeat',  # Supraventricular premature
        2: 'arrhythmia',  # Ventricular ectopic
        3: 'abnormal_heartbeat',  # Fusion beat
        4: 'arrhythmia'   # Unknown
    }
    
    # Create directory structure
    base_dir = 'datasets/ecg'
    for split in ['train', 'val']:
        for class_name in ['normal', 'abnormal_heartbeat', 'arrhythmia', 
                          'myocardial_infarction', 'history_of_mi']:
            os.makedirs(f'{base_dir}/{split}/{class_name}', exist_ok=True)
    
    # Split data
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Convert ECG signals to images
    def ecg_to_image(signal, filename):
        plt.figure(figsize=(6, 4))
        plt.plot(signal, linewidth=2, color='black')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(filename, bbox_inches='tight', pad_inches=0)
        plt.close()
    
    # Save training images
    print("Converting ECG signals to images (Train)...")
    for idx, (signal, label) in enumerate(zip(X_train, y_train)):
        class_name = class_mapping[label]
        filename = f'{base_dir}/train/{class_name}/ecg_{idx}.png'
        ecg_to_image(signal, filename)
        if idx % 1000 == 0:
            print(f"Processed {idx}/{len(X_train)} training samples")
    
    # Save validation images
    print("Converting ECG signals to images (Val)...")
    for idx, (signal, label) in enumerate(zip(X_val, y_val)):
        class_name = class_mapping[label]
        filename = f'{base_dir}/val/{class_name}/ecg_{idx}.png'
        ecg_to_image(signal, filename)
        if idx % 1000 == 0:
            print(f"Processed {idx}/{len(X_val)} validation samples")
    
    print("ECG dataset preparation complete!")
    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")

def download_from_kaggle():
    """Download datasets using Kaggle API"""
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        
        api = KaggleApi()
        api.authenticate()
        
        print("Downloading ECG Heartbeat Dataset...")
        api.dataset_download_files(
            'shayanfazeli/heartbeat',
            path='temp_ecg',
            unzip=True
        )
        print("Download complete!")
        
    except Exception as e:
        print(f"Error downloading from Kaggle: {e}")
        print("\nPlease download manually:")
        print("1. Go to https://www.kaggle.com/datasets/shayanfazeli/heartbeat")
        print("2. Click 'Download' button")
        print("3. Extract to 'temp_ecg' folder")

if __name__ == '__main__':
    print("Heart Disease Analyzer - Dataset Preparation")
    print("="*60)
    
    choice = input("\n1. Download from Kaggle (requires API setup)\n2. I've already downloaded manually\nChoice (1/2): ")
    
    if choice == '1':
        download_from_kaggle()
    
    if os.path.exists('temp_ecg/mitbih_train.csv'):
        prepare_ecg_heartbeat_dataset()
    else:
        print("\nDataset files not found!")
        print("Please download manually and try again.")
```

## 🎯 Training with Kaggle Dataset

### Updated Training Script

Update your `train_models.py` to use the new 5-class classification:

```python
# The model is already updated in app.py
# Just run the training with proper dataset structure

python train_models.py
```

### Training Process

1. **Prepare Dataset**:
   ```bash
   python prepare_kaggle_dataset.py
   ```

2. **Verify Dataset Structure**:
   ```bash
   # Check if all folders exist
   dir datasets\ecg\train
   dir datasets\ecg\val
   ```

3. **Start Training**:
   ```bash
   python train_models.py
   ```

4. **Monitor Training**:
   - Watch accuracy/loss in console
   - Check `models/` folder for saved models
   - View training plots after completion

## 📊 Expected Results

### ECG Model
- **Input**: ECG signal images (128x128)
- **Output**: 5 classes
  - Normal
  - Myocardial Infarction
  - Abnormal Heartbeat
  - History of MI
  - Arrhythmia
- **Expected Accuracy**: 85-95% (depending on dataset quality)

### MRI Model
- **Input**: Cardiac MRI images (128x128)
- **Output**: 5 classes
  - Normal
  - Cardiomyopathy
  - Coronary Artery Disease
  - Heart Failure
  - Myocardial Infarction
- **Expected Accuracy**: 80-90%

## 🔍 Data Augmentation Tips

For better model performance:

```python
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Enhanced augmentation
datagen = ImageDataGenerator(
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=False,  # Don't flip ECG/MRI
    fill_mode='nearest',
    brightness_range=[0.8, 1.2],
    preprocessing_function=lambda x: x / 255.0
)
```

## ⚡ Quick Start Commands

```bash
# 1. Install Kaggle API
pip install kaggle

# 2. Setup credentials (place kaggle.json in ~/.kaggle/)

# 3. Download dataset preparation script
python prepare_kaggle_dataset.py

# 4. Train models
python train_models.py

# 5. Start web application
python app.py
```

## 📝 Important Notes

1. **Dataset Size**: Large datasets may take hours to process
2. **RAM Requirements**: Ensure 8GB+ RAM for processing
3. **GPU Recommended**: Training is much faster with GPU
4. **Storage**: ECG dataset alone can be 5-10GB after conversion
5. **Data License**: Check Kaggle dataset licenses before commercial use

## 🆘 Troubleshooting

### "401 Unauthorized" Error
- Verify kaggle.json is in correct location
- Check API token is valid
- Re-download credentials from Kaggle

### Out of Memory
- Reduce batch size in training script
- Process dataset in smaller batches
- Use data generators instead of loading all data

### Slow Download
- Use Kaggle CLI instead of API
- Download manually from browser
- Check internet connection

## 🎓 Additional Resources

- **Kaggle Datasets**: https://www.kaggle.com/datasets
- **TensorFlow Tutorials**: https://www.tensorflow.org/tutorials
- **Medical Image Processing**: https://www.pyimagesearch.com/

---

**Ready to train?** Follow the steps above and your model will be ready to detect heart diseases from real medical images!
