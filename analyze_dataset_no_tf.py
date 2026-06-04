"""
Dataset analyzer that works without TensorFlow
Helps organize your ECG dataset for later training
"""

import os
import shutil
from pathlib import Path
import random
from collections import defaultdict

def analyze_and_organize_dataset(dataset_path, output_name="varun_ecg"):
    """
    Analyze and organize ECG dataset without TensorFlow
    Creates proper folder structure for future training
    """
    
    print("=" * 60)
    print(f"Analyzing and Organizing ECG Dataset: {output_name}")
    print("=" * 60)
    
    dataset_path = Path(dataset_path)
    
    if not dataset_path.exists():
        print(f"❌ Error: Dataset path not found: {dataset_path}")
        return False
    
    # Create output directory structure
    base_output = Path(f'datasets/{output_name}')
    classes = ['normal', 'myocardial_infarction', 'abnormal_heartbeat', 
              'history_of_mi', 'arrhythmia']
    
    print("📁 Creating directory structure...")
    for split in ['train', 'val']:
        for class_name in classes:
            (base_output / split / class_name).mkdir(parents=True, exist_ok=True)
    
    # Find all image files
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}
    all_images = []
    
    print(f"\n🔍 Scanning dataset at: {dataset_path}")
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(dataset_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                all_images.append(Path(root) / file)
    
    print(f"📊 Found {len(all_images)} ECG images")
    
    if len(all_images) == 0:
        print("❌ No images found in dataset!")
        return False
    
    # Try to categorize based on folder names or filenames
    categorized = defaultdict(list)
    
    # Simple heuristic: look for keywords in paths
    for img_path in all_images:
        path_str = str(img_path).lower()
        
        # Try to guess category from path
        if any(keyword in path_str for keyword in ['normal', 'healthy']):
            categorized['normal'].append(img_path)
        elif any(keyword in path_str for keyword in ['mi', 'infarction', 'heart_attack']):
            categorized['myocardial_infarction'].append(img_path)
        elif any(keyword in path_str for keyword in ['abnormal', 'arrhythmia']):
            categorized['abnormal_heartbeat'].append(img_path)
        elif any(keyword in path_str for keyword in ['history', 'previous']):
            categorized['history_of_mi'].append(img_path)
        elif any(keyword in path_str for keyword in ['arr', 'rhythm']):
            categorized['arrhythmia'].append(img_path)
        else:
            # Put in normal by default
            categorized['normal'].append(img_path)
    
    # Report categorization
    print(f"\n📋 Categorization Results:")
    for category, images in categorized.items():
        print(f"  {category}: {len(images)} images")
    
    # Distribute to train/val splits
    print(f"\n📂 Organizing into train/validation splits...")
    
    total_copied = 0
    for category, images in categorized.items():
        if not images:
            continue
            
        # Shuffle and split (80/20)
        random.shuffle(images)
        split_point = int(0.8 * len(images))
        
        train_images = images[:split_point]
        val_images = images[split_point:]
        
        # Copy to respective folders
        for img_path in train_images:
            try:
                target_path = base_output / 'train' / category / img_path.name
                shutil.copy2(img_path, target_path)
                total_copied += 1
            except Exception as e:
                print(f"⚠️  Warning copying {img_path}: {e}")
        
        for img_path in val_images:
            try:
                target_path = base_output / 'val' / category / img_path.name
                shutil.copy2(img_path, target_path)
                total_copied += 1
            except Exception as e:
                print(f"⚠️  Warning copying {img_path}: {e}")
    
    print(f"\n✅ Successfully organized {total_copied} images!")
    print(f"📁 Output location: {base_output}")
    
    # Show final structure
    print(f"\n📂 Final Dataset Structure:")
    for split in ['train', 'val']:
        print(f"  {split}/")
        for class_name in classes:
            count = len(list((base_output / split / class_name).glob('*')))
            if count > 0:
                print(f"    {class_name}/ ({count} images)")
    
    print(f"\n{'='*60}")
    print("🎉 Dataset Analysis and Organization COMPLETE!")
    print("=" * 60)
    print(f"\nWhen TensorFlow is working, you can train with:")
    print(f"python train_models.py")
    print(f"\nYour dataset is ready at: datasets/{output_name}")
    
    return True

def main():
    print("ECG Dataset Analyzer (No TensorFlow Required)")
    print("=" * 50)
    
    # Default path for your dataset
    default_path = r"C:\Users\VARUN COMPUTERS\Desktop\7th SEM\Dataset"
    
    if os.path.exists(default_path):
        print(f"✅ Found your dataset folder!")
        use_default = input(f"Use '{default_path}'? (Y/n): ").strip().lower()
        if use_default != 'n':
            dataset_path = default_path
        else:
            dataset_path = input("Enter path to your ECG dataset: ").strip()
    else:
        dataset_path = input("Enter path to your ECG dataset: ").strip()
    
    if not dataset_path or not os.path.exists(dataset_path):
        print("❌ Invalid path. Exiting.")
        return
    
    # Analyze and organize
    success = analyze_and_organize_dataset(dataset_path)
    
    if success:
        print(f"\n🚀 Next steps when TensorFlow works:")
        print(f"1. Fix TensorFlow installation")
        print(f"2. Run: python train_models.py")
        print(f"3. Your dataset is already organized!")

if __name__ == '__main__':
    main()
