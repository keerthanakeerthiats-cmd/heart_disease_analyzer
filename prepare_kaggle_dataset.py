"""
Automated script to download and prepare Kaggle datasets for Heart Disease Analyzer
Supports ECG Heartbeat Categorization Dataset from Kaggle
"""

import os
import shutil
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
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
    train_file = 'temp_ecg/mitbih_train.csv'
    test_file = 'temp_ecg/mitbih_test.csv'
    
    if not os.path.exists(train_file) or not os.path.exists(test_file):
        print("Dataset not found. Please download manually from:")
        print("https://www.kaggle.com/datasets/shayanfazeli/heartbeat")
        print("\nDownload and extract to 'temp_ecg' folder")
        return False
    
    print("Loading dataset files...")
    # Load the data
    train_df = pd.read_csv(train_file, header=None)
    test_df = pd.read_csv(test_file, header=None)
    
    # Combine train and test
    all_data = pd.concat([train_df, test_df], ignore_index=True)
    
    print(f"Total samples: {len(all_data)}")
    
    # Separate features and labels
    X = all_data.iloc[:, :-1].values
    y = all_data.iloc[:, -1].values.astype(int)
    
    # Class mapping (original dataset has 5 classes: 0-4)
    # We'll map these to our 5 disease categories
    class_mapping = {
        0: 'normal',                    # Normal beat
        1: 'abnormal_heartbeat',        # Supraventricular premature beat
        2: 'arrhythmia',               # Ventricular ectopic beat
        3: 'history_of_mi',            # Fusion beat (can indicate previous MI)
        4: 'myocardial_infarction'     # Unclassifiable (potential MI)
    }
    
    # Print class distribution
    print("\nClass distribution:")
    unique, counts = np.unique(y, return_counts=True)
    for cls, count in zip(unique, counts):
        print(f"  {class_mapping[cls]}: {count} samples")
    
    # Create directory structure
    base_dir = 'datasets/ecg'
    print("\nCreating directory structure...")
    for split in ['train', 'val']:
        for class_name in ['normal', 'abnormal_heartbeat', 'arrhythmia', 
                          'myocardial_infarction', 'history_of_mi']:
            os.makedirs(f'{base_dir}/{split}/{class_name}', exist_ok=True)
    
    # Split data - stratified to maintain class distribution
    print("\nSplitting dataset (80% train, 20% validation)...")
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    
    # Convert ECG signals to images
    def ecg_to_image(signal, filename, dpi=100):
        """Convert ECG signal to image"""
        fig = plt.figure(figsize=(8, 6), dpi=dpi)
        
        # Plot ECG signal
        plt.plot(signal, linewidth=2, color='black')
        plt.ylim([signal.min() - 0.5, signal.max() + 0.5])
        plt.xlim([0, len(signal)])
        
        # Add grid (like real ECG paper)
        plt.grid(True, which='both', linestyle='-', linewidth=0.5, color='red', alpha=0.3)
        
        # Remove axes
        plt.axis('off')
        plt.tight_layout(pad=0)
        
        # Save with white background
        plt.savefig(filename, bbox_inches='tight', pad_inches=0.1, 
                   facecolor='white', edgecolor='none')
        plt.close(fig)
    
    # Save training images
    print("\nConverting ECG signals to images (Training set)...")
    for idx, (signal, label) in enumerate(zip(X_train, y_train)):
        class_name = class_mapping[label]
        filename = f'{base_dir}/train/{class_name}/ecg_{idx}.png'
        ecg_to_image(signal, filename)
        
        if (idx + 1) % 1000 == 0:
            print(f"  Processed {idx + 1}/{len(X_train)} training samples")
    
    print(f"  Completed: {len(X_train)} training images")
    
    # Save validation images
    print("\nConverting ECG signals to images (Validation set)...")
    for idx, (signal, label) in enumerate(zip(X_val, y_val)):
        class_name = class_mapping[label]
        filename = f'{base_dir}/val/{class_name}/ecg_{idx}.png'
        ecg_to_image(signal, filename)
        
        if (idx + 1) % 1000 == 0:
            print(f"  Processed {idx + 1}/{len(X_val)} validation samples")
    
    print(f"  Completed: {len(X_val)} validation images")
    
    print("\n" + "="*60)
    print("ECG dataset preparation COMPLETE!")
    print("="*60)
    print(f"\nDataset location: {base_dir}/")
    print("\nYou can now train the model using: python train_models.py")
    
    return True

def download_from_kaggle():
    """Download datasets using Kaggle API"""
    try:
        print("Attempting to download from Kaggle using API...")
        from kaggle.api.kaggle_api_extended import KaggleApi
        
        api = KaggleApi()
        api.authenticate()
        
        print("\nDownloading ECG Heartbeat Dataset...")
        print("This may take several minutes depending on your connection...")
        
        # Create temp directory
        os.makedirs('temp_ecg', exist_ok=True)
        
        api.dataset_download_files(
            'shayanfazeli/heartbeat',
            path='temp_ecg',
            unzip=True
        )
        
        print("\n✓ Download complete!")
        return True
        
    except ImportError:
        print("\nKaggle API not installed!")
        print("Install with: pip install kaggle")
        return False
    except Exception as e:
        print(f"\nError downloading from Kaggle: {e}")
        print("\nPlease download manually:")
        print("1. Go to https://www.kaggle.com/datasets/shayanfazeli/heartbeat")
        print("2. Click 'Download' button")
        print("3. Extract to 'temp_ecg' folder in this directory")
        return False

def check_kaggle_credentials():
    """Check if Kaggle API credentials are configured"""
    kaggle_json_path = os.path.join(os.path.expanduser('~'), '.kaggle', 'kaggle.json')
    
    if not os.path.exists(kaggle_json_path):
        print("\n⚠️  Kaggle API credentials not found!")
        print("\nTo setup Kaggle API:")
        print("1. Go to https://www.kaggle.com/")
        print("2. Click on your profile → Account")
        print("3. Scroll to 'API' section → Create New API Token")
        print("4. Download kaggle.json")
        print("5. Place it in: " + kaggle_json_path)
        return False
    
    print("✓ Kaggle credentials found")
    return True

def main():
    print("\n" + "="*60)
    print("Heart Disease Analyzer - Kaggle Dataset Preparation")
    print("="*60)
    
    print("\nThis script will:")
    print("1. Download ECG Heartbeat dataset from Kaggle (optional)")
    print("2. Convert ECG signals to images")
    print("3. Organize into training/validation folders")
    print("4. Prepare for model training")
    
    print("\n" + "="*60)
    
    # Check if dataset already exists
    if os.path.exists('temp_ecg/mitbih_train.csv'):
        print("\n✓ Dataset files found in temp_ecg/")
        choice = input("\nProceed with dataset preparation? (y/n): ").lower()
        if choice == 'y':
            prepare_ecg_heartbeat_dataset()
        return
    
    # Ask user for download preference
    print("\nDataset not found locally.")
    print("\nOptions:")
    print("1. Download from Kaggle using API (requires setup)")
    print("2. I'll download manually")
    
    choice = input("\nChoice (1/2): ").strip()
    
    if choice == '1':
        if check_kaggle_credentials():
            if download_from_kaggle():
                print("\nProceeding with dataset preparation...")
                prepare_ecg_heartbeat_dataset()
            else:
                print("\nDownload failed. Please try manual download.")
        else:
            print("\nPlease setup Kaggle API credentials and try again.")
            print("Or choose manual download option.")
    
    elif choice == '2':
        print("\n" + "="*60)
        print("Manual Download Instructions")
        print("="*60)
        print("\n1. Visit: https://www.kaggle.com/datasets/shayanfazeli/heartbeat")
        print("2. Click the 'Download' button (you may need to sign in)")
        print("3. Extract the downloaded ZIP file")
        print("4. Create a folder named 'temp_ecg' in this directory")
        print("5. Copy the CSV files to temp_ecg/ folder")
        print("6. Run this script again")
        print("\nExpected files:")
        print("  - temp_ecg/mitbih_train.csv")
        print("  - temp_ecg/mitbih_test.csv")
    else:
        print("\nInvalid choice. Exiting.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
