"""
Advanced dataset scanner that can handle various ECG dataset structures
"""

import os
import zipfile
from pathlib import Path
import shutil
from collections import defaultdict
import random

def advanced_scan_dataset(dataset_path):
    """
    Advanced scan that looks deeper into folders and handles ZIP files
    """
    print("=" * 60)
    print("Advanced ECG Dataset Scanner")
    print("=" * 60)
    
    dataset_path = Path(dataset_path)
    
    if not dataset_path.exists():
        print(f"❌ Dataset path not found: {dataset_path}")
        return []
    
    print(f"🔍 Scanning: {dataset_path}")
    
    # Supported image extensions
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}
    
    # All found images
    all_images = []
    
    # First, check if there are ZIP files to extract
    zip_files = list(dataset_path.glob("*.zip"))
    if zip_files:
        print(f"\n📦 Found {len(zip_files)} ZIP files:")
        for zip_file in zip_files:
            print(f"  - {zip_file.name}")
            
            # Extract to temporary folder
            extract_folder = dataset_path / f"extracted_{zip_file.stem}"
            if not extract_folder.exists():
                print(f"    Extracting {zip_file.name}...")
                try:
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        zip_ref.extractall(extract_folder)
                    print(f"    ✓ Extracted to {extract_folder}")
                except Exception as e:
                    print(f"    ❌ Failed to extract: {e}")
    
    # Now scan recursively through all folders
    print(f"\n🔄 Recursive scan of all folders...")
    
    for root, dirs, files in os.walk(dataset_path):
        # Skip already processed extracted folders to avoid duplicates
        if "extracted_" in root and len(Path(root).parts) > len(dataset_path.parts) + 1:
            continue
            
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                full_path = Path(root) / file
                all_images.append(full_path)
    
    print(f"\n📊 Total images found: {len(all_images)}")
    
    if all_images:
        print(f"\n📋 Sample images found:")
        for i, img in enumerate(all_images[:10]):
            print(f"  {i+1}. {img}")
        if len(all_images) > 10:
            print(f"  ... and {len(all_images) - 10} more")
    
    return all_images

def organize_with_manual_categorization(images):
    """
    Let user manually categorize if automatic fails
    """
    print(f"\n{'='*60}")
    print("MANUAL CATEGORIZATION NEEDED")
    print("=" * 60)
    
    if not images:
        print("❌ No images to categorize")
        return False
    
    # Show first few images
    print(f"\n📋 First 5 images:")
    for i, img in enumerate(images[:5]):
        print(f"  {i+1}. {img.name}")
    
    print(f"\n📁 Dataset structure options:")
    print("1. All images are NORMAL (healthy)")
    print("2. All images are MYOCARDIAL INFARCTION (heart attack)")
    print("3. All images are ABNORMAL HEARTBEAT")
    print("4. All images are ARRHYTHMIA")
    print("5. Mixed - I'll categorize samples")
    print("6. Skip categorization (put all in normal for now)")
    
    choice = input("\nEnter your choice (1-6): ").strip()
    
    category_map = {
        '1': 'normal',
        '2': 'myocardial_infarction',
        '3': 'abnormal_heartbeat',
        '4': 'arrhythmia',
        '6': 'normal'
    }
    
    if choice in category_map:
        target_category = category_map[choice]
        print(f"\n📁 Putting all {len(images)} images in '{target_category}' category")
        return [(img, target_category) for img in images]
    
    elif choice == '5':
        # Manual sample categorization
        categorized = []
        print(f"\n🎯 Manual categorization of samples:")
        print("Categories: normal, myocardial_infarction, abnormal_heartbeat, history_of_mi, arrhythmia")
        
        for i, img in enumerate(images[:10]):  # First 10 images
            print(f"\n{i+1}. {img.name}")
            category = input("Category (or press Enter for 'normal'): ").strip().lower()
            if not category:
                category = 'normal'
            if category not in ['normal', 'myocardial_infarction', 'abnormal_heartbeat', 'history_of_mi', 'arrhythmia']:
                category = 'normal'
            categorized.append((img, category))
        
        # Apply same pattern to rest or put in normal
        for img in images[10:]:
            categorized.append((img, 'normal'))
        
        return categorized
    
    else:
        print("Invalid choice. Putting all in 'normal' category.")
        return [(img, 'normal') for img in images]

def organize_dataset_advanced(dataset_path, output_name="varun_ecg"):
    """
    Advanced organizer that handles various dataset structures
    """
    print("=" * 60)
    print(f"Advanced Dataset Organizer: {output_name}")
    print("=" * 60)
    
    # Scan for images
    images = advanced_scan_dataset(dataset_path)
    
    if not images:
        print(f"\n❌ No images found in dataset!")
        print(f"\n💡 Troubleshooting tips:")
        print(f"   1. Check if files are in ZIP archives that need extraction")
        print(f"   2. Check if images are in subfolders")
        print(f"   3. Verify file extensions (PNG, JPG, etc.)")
        print(f"   4. Check if folder permissions allow reading")
        return False
    
    # Try automatic categorization first
    categorized_images = []
    
    # Simple automatic categorization based on path keywords
    category_keywords = {
        'normal': ['normal', 'healthy', 'control'],
        'myocardial_infarction': ['mi', 'infarction', 'heart_attack', 'myocardial'],
        'abnormal_heartbeat': ['abnormal', 'beat'],
        'history_of_mi': ['history', 'previous', 'past'],
        'arrhythmia': ['arrhythmia', 'arr', 'rhythm']
    }
    
    uncategorized = []
    
    for img in images:
        path_lower = str(img).lower()
        categorized = False
        
        for category, keywords in category_keywords.items():
            if any(keyword in path_lower for keyword in keywords):
                categorized_images.append((img, category))
                categorized = True
                break
        
        if not categorized:
            uncategorized.append(img)
    
    # Handle uncategorized images
    if uncategorized:
        print(f"\n❓ Found {len(uncategorized)} images that couldn't be auto-categorized")
        print("   They will be put in 'normal' category by default")
        for img in uncategorized:
            categorized_images.append((img, 'normal'))
    
    # Report categorization
    category_counts = defaultdict(int)
    for _, category in categorized_images:
        category_counts[category] += 1
    
    print(f"\n📊 Auto-categorization results:")
    for category, count in category_counts.items():
        print(f"  {category}: {count} images")
    
    # Create output structure
    base_output = Path(f'datasets/{output_name}')
    classes = ['normal', 'myocardial_infarction', 'abnormal_heartbeat', 'history_of_mi', 'arrhythmia']
    
    print(f"\n📁 Creating output directory structure...")
    for split in ['train', 'val']:
        for class_name in classes:
            (base_output / split / class_name).mkdir(parents=True, exist_ok=True)
    
    # Distribute images
    print(f"\n📂 Organizing images into train/validation splits...")
    
    # Group by category
    by_category = defaultdict(list)
    for img_path, category in categorized_images:
        by_category[category].append(img_path)
    
    total_copied = 0
    
    for category, img_list in by_category.items():
        if not img_list:
            continue
        
        # Shuffle and split (80/20)
        random.shuffle(img_list)
        split_point = int(0.8 * len(img_list))
        
        train_images = img_list[:split_point]
        val_images = img_list[split_point:]
        
        # Copy train images
        for img_path in train_images:
            try:
                target_path = base_output / 'train' / category / img_path.name
                if not target_path.exists():  # Avoid duplicates
                    shutil.copy2(img_path, target_path)
                total_copied += 1
            except Exception as e:
                print(f"⚠️  Warning copying {img_path.name}: {e}")
        
        # Copy validation images
        for img_path in val_images:
            try:
                target_path = base_output / 'val' / category / img_path.name
                if not target_path.exists():  # Avoid duplicates
                    shutil.copy2(img_path, target_path)
                total_copied += 1
            except Exception as e:
                print(f"⚠️  Warning copying {img_path.name}: {e}")
    
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
    print("🎉 Advanced Dataset Organization COMPLETE!")
    print("=" * 60)
    print(f"\nWhen ready, train with: python train_models.py")
    
    return True

def main():
    print("Advanced ECG Dataset Organizer")
    print("=" * 40)
    
    # Default path
    default_path = r"C:\Users\VARUN COMPUTERS\Desktop\7th SEM\Dataset"
    
    if os.path.exists(default_path):
        print(f"✅ Found dataset folder: {default_path}")
        use_default = input("Use this folder? (Y/n): ").strip().lower()
        if use_default != 'n':
            dataset_path = default_path
        else:
            dataset_path = input("Enter path to your ECG dataset: ").strip()
    else:
        dataset_path = input("Enter path to your ECG dataset: ").strip()
    
    if not dataset_path or not os.path.exists(dataset_path):
        print("❌ Invalid path. Exiting.")
        return
    
    # Organize dataset
    success = organize_dataset_advanced(dataset_path)
    
    if success:
        print(f"\n🚀 Next steps:")
        print(f"1. Run: python train_models.py")
        print(f"2. Your dataset is organized and ready!")

if __name__ == '__main__':
    main()
