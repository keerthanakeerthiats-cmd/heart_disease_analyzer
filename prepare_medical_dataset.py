"""
Dataset Preparation Script for Heart Disease Analyzer
Helps organize medical images into proper training and validation directories
"""

import os
import shutil
import random
from pathlib import Path

def create_dataset_structure(base_path):
    """Create the required directory structure for the dataset"""
    # ECG dataset structure
    ecg_train_dirs = [
        "datasets/varun_ecg/train/normal",
        "datasets/varun_ecg/train/myocardial_infarction", 
        "datasets/varun_ecg/train/abnormal_heartbeat",
        "datasets/varun_ecg/train/history_of_mi",
        "datasets/varun_ecg/train/arrhythmia"
    ]
    
    ecg_val_dirs = [
        "datasets/varun_ecg/val/normal",
        "datasets/varun_ecg/val/myocardial_infarction",
        "datasets/varun_ecg/val/abnormal_heartbeat", 
        "datasets/varun_ecg/val/history_of_mi",
        "datasets/varun_ecg/val/arrhythmia"
    ]
    
    # MRI dataset structure
    mri_train_dirs = [
        "datasets/varun_mri/train/normal",
        "datasets/varun_mri/train/cardiomyopathy",
        "datasets/varun_mri/train/coronary_artery_disease",
        "datasets/varun_mri/train/heart_failure",
        "datasets/varun_mri/train/myocardial_infarction"
    ]
    
    mri_val_dirs = [
        "datasets/varun_mri/val/normal",
        "datasets/varun_mri/val/cardiomyopathy",
        "datasets/varun_mri/val/coronary_artery_disease",
        "datasets/varun_mri/val/heart_failure",
        "datasets/varun_mri/val/myocardial_infarction"
    ]
    
    # Create all directories
    all_dirs = ecg_train_dirs + ecg_val_dirs + mri_train_dirs + mri_val_dirs
    
    for directory in all_dirs:
        os.makedirs(os.path.join(base_path, directory), exist_ok=True)
        print(f"Created directory: {directory}")

def organize_existing_dataset(source_path, destination_base, train_ratio=0.8):
    """
    Organize existing dataset from a source directory
    Assumes source directory has subdirectories named after classes
    """
    if not os.path.exists(source_path):
        print(f"Source path {source_path} does not exist")
        return
    
    class_dirs = [d for d in os.listdir(source_path) if os.path.isdir(os.path.join(source_path, d))]
    
    for class_name in class_dirs:
        class_path = os.path.join(source_path, class_name)
        images = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Shuffle images
        random.shuffle(images)
        
        # Split into train and validation
        split_idx = int(len(images) * train_ratio)
        train_images = images[:split_idx]
        val_images = images[split_idx:]
        
        # Move train images
        train_dest = os.path.join(destination_base, "train", class_name.lower().replace(" ", "_"))
        for img in train_images:
            src = os.path.join(class_path, img)
            dst = os.path.join(train_dest, img)
            shutil.copy2(src, dst)
        
        # Move validation images
        val_dest = os.path.join(destination_base, "val", class_name.lower().replace(" ", "_"))
        for img in val_images:
            src = os.path.join(class_path, img)
            dst = os.path.join(val_dest, img)
            shutil.copy2(src, dst)
        
        print(f"Organized {class_name}: {len(train_images)} train, {len(val_images)} validation")

def download_sample_dataset():
    """
    Instructions for downloading sample medical datasets
    """
    print("\n" + "="*60)
    print("SAMPLE DATASET SOURCES")
    print("="*60)
    print("""
    1. Kaggle ECG Dataset:
       - https://www.kaggle.com/shayanfazeli/heartbeat
       - Contains ECG recordings for arrhythmia detection
       
    2. PhysioNet MIT-BIH Arrhythmia Database:
       - https://physionet.org/content/mitdb/1.0.0/
       - Standard dataset for ECG arrhythmia analysis
       
    3. Kaggle Chest X-ray Dataset (for heart conditions):
       - https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia
       - Can be adapted for heart disease detection
       
    4. MIMIC-CXR Database:
       - https://physionet.org/content/mimic-cxr/2.0.0/
       - Large dataset of chest X-rays with reports
       
    To use these datasets:
    1. Download the dataset
    2. Extract the files
    3. Run this script to organize them:
       python prepare_medical_dataset.py --organize path/to/downloaded/dataset
    """)

def main():
    """Main function"""
    print("Heart Disease Analyzer Dataset Preparation Tool")
    print("=" * 50)
    
    # Create dataset structure
    create_dataset_structure(".")
    
    print("\nDataset structure created successfully!")
    print("\nNext steps:")
    print("1. Collect medical images for each condition")
    print("2. Place images in the appropriate directories:")
    print("   - datasets/varun_ecg/train/[condition]/ for ECG training images")
    print("   - datasets/varun_ecg/val/[condition]/ for ECG validation images")
    print("   - datasets/varun_mri/train/[condition]/ for MRI training images")
    print("   - datasets/varun_mri/val/[condition]/ for MRI validation images")
    
    download_sample_dataset()

if __name__ == "__main__":
    main()