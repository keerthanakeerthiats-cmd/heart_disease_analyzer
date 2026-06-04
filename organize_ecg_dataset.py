"""
Script to organize your ECG dataset for training
Supports various ECG dataset formats
"""

import os
import zipfile
import shutil
from pathlib import Path
import random
import sys

def organize_ecg_dataset(dataset_path, dataset_name="custom_ecg"):
    """
    Organize ECG dataset into proper folder structure for training
    
    Expected input structure (any of these):
    dataset_folder/
        ├── normal/
        ├── mi/ or myocardial_infarction/
        ├── abnormal/ or abnormal_heartbeat/
        ├── arrhythmia/
        └── ...
    
    OR
    
    dataset_folder/
        ├── patient1_ecg.png
        ├── patient2_ecg.jpg
        └── labels.csv (with disease labels)
    """
    
    print("=" * 60)
    print(f"Organizing ECG Dataset: {dataset_name}")
    print("=" * 60)
    
    # Create proper directory structure
    base_dir = f'datasets/{dataset_name}'
    classes = ['normal', 'myocardial_infarction', 'abnormal_heartbeat', 
              'history_of_mi', 'arrhythmia']
    
    print("Creating directory structure...")
    for split in ['train', 'val']:
        for class_name in classes:
            os.makedirs(f'{base_dir}/{split}/{class_name}', exist_ok=True)
    
    # Check if it's a ZIP file
    if dataset_path.endswith('.zip'):
        print(f"\nExtracting ZIP file: {dataset_path}")
        with zipfile.ZipFile(dataset_path, 'r') as zip_ref:
            extract_path = f'temp_{dataset_name}'
            zip_ref.extractall(extract_path)
            dataset_path = extract_path
    
    # Analyze dataset structure
    dataset_path = Path(dataset_path)
    
    if not dataset_path.exists():
        print(f"Error: Dataset path not found: {dataset_path}")
        return False
    
    # Try to detect dataset structure
    print(f"\nAnalyzing dataset at: {dataset_path}")
    
    # Method 1: Already organized folders
    class_folders = [f for f in dataset_path.iterdir() if f.is_dir()]
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}
    
    if class_folders:
        print("Found organized class folders:")
        for folder in class_folders:
            print(f"  - {folder.name}")
        
        # Map folder names to our classes
        class_mapping = {
            'normal': 'normal',
            'n': 'normal',
            'healthy': 'normal',
            'mi': 'myocardial_infarction',
            'myocardial_infarction': 'myocardial_infarction',
            'heart_attack': 'myocardial_infarction',
            'abnormal': 'abnormal_heartbeat',
            'abnormal_heartbeat': 'abnormal_heartbeat',
            'arrhythmia': 'arrhythmia',
            'arr': 'arrhythmia',
            'history_of_mi': 'history_of_mi',
            'previous_mi': 'history_of_mi'
        }
        
        # Process each class folder
        for folder in class_folders:
            folder_name = folder.name.lower()
            target_class = None
            
            # Try exact match
            if folder_name in class_mapping:
                target_class = class_mapping[folder_name]
            else:
                # Try partial match
                for key, value in class_mapping.items():
                    if key in folder_name or folder_name in key:
                        target_class = value
                        break
            
            if target_class:
                print(f"\nProcessing {folder_name} → {target_class}")
                
                # Get all image files
                image_files = []
                for ext in image_extensions:
                    image_files.extend(folder.glob(f'*{ext}'))
                    image_files.extend(folder.glob(f'*{ext.upper()}'))
                
                print(f"  Found {len(image_files)} images")
                
                # Split into train/val (80/20)
                random.shuffle(image_files)
                split_idx = int(0.8 * len(image_files))
                
                train_files = image_files[:split_idx]
                val_files = image_files[split_idx:]
                
                # Copy files
                for file in train_files:
                    target_path = f'{base_dir}/train/{target_class}/{file.name}'
                    shutil.copy2(file, target_path)
                
                for file in val_files:
                    target_path = f'{base_dir}/val/{target_class}/{file.name}'
                    shutil.copy2(file, target_path)
                
                print(f"  Copied {len(train_files)} to train, {len(val_files)} to val")
            else:
                print(f"  Skipping unknown folder: {folder_name}")
    
    else:
        # Method 2: Flat structure with images
        print("Found flat image structure")
        image_files = []
        for ext in image_extensions:
            image_files.extend(dataset_path.glob(f'*{ext}'))
            image_files.extend(dataset_path.glob(f'*{ext.upper()}'))
        
        print(f"Found {len(image_files)} images")
        
        if image_files:
            # Ask user for labeling or use random distribution for demo
            print("\nHow would you like to organize these images?")
            print("1. Random distribution (for testing)")
            print("2. Manual labeling (coming soon)")
            
            choice = input("Choice (1/2): ").strip()
            
            if choice == '1':
                # Random distribution for testing
                random.shuffle(image_files)
                split_idx = int(0.8 * len(image_files))
                
                # Distribute randomly among classes
                classes_cycle = ['normal', 'myocardial_infarction', 'abnormal_heartbeat', 
                               'history_of_mi', 'arrhythmia']
                
                for i, file in enumerate(image_files):
                    target_class = classes_cycle[i % len(classes_cycle)]
                    split = 'train' if i < split_idx else 'val'
                    target_path = f'{base_dir}/{split}/{target_class}/{file.name}'
                    shutil.copy2(file, target_path)
                
                print(f"Organized {len(image_files)} images randomly")
    
    print(f"\nDataset organized at: {base_dir}")
    print("\nDirectory structure:")
    for split in ['train', 'val']:
        print(f"  {split}/")
        for class_name in classes:
            count = len(list(Path(f'{base_dir}/{split}/{class_name}').glob('*')))
            print(f"    {class_name}/ ({count} images)")
    
    print("\n" + "=" * 60)
    print("Dataset organization COMPLETE!")
    print("=" * 60)
    print(f"\nYou can now train models with:")
    print(f"python train_models.py")
    
    return True

def main():
    print("ECG Dataset Organizer")
    print("=" * 30)
    
    # Default paths for VARUN's dataset
    default_path = r"C:\\Users\\VARUN COMPUTERS\\Desktop\\7th SEM\\Dataset"
    print(f"Default dataset location: {default_path}")
    
    # Check if default path exists
    if os.path.exists(default_path):
        print("✓ Found your dataset folder!")
        dataset_path = default_path
        use_default = input("Use this folder? (Y/n): ").strip().lower()
        if use_default == 'n':
            dataset_path = input("Enter path to your ECG dataset (ZIP file or folder): ").strip()
    else:
        # Ask for dataset path
        dataset_path = input("Enter path to your ECG dataset (ZIP file or folder): ").strip()
    
    if not dataset_path:
        print("No path provided. Exiting.")
        return
    
    # Ask for dataset name
    dataset_name = input("Enter dataset name (default: varun_ecg): ").strip()
    if not dataset_name:
        dataset_name = "varun_ecg"
    
    # Organize dataset
    success = organize_ecg_dataset(dataset_path, dataset_name)
    
    if success:
        print(f"\n✅ Dataset ready for training!")
        print(f"\nNext steps:")
        print(f"1. Run: python train_models.py")
        print(f"2. Models will be saved to: models/")
        print(f"3. Use: python app.py for real predictions")

if __name__ == '__main__':
    main()
