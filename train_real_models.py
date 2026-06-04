"""
Real AI Model Trainer for Heart Disease Analyzer
Trains CNN models for ECG and MRI image classification
"""

import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from PIL import Image
import json
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def create_ecg_model(num_classes=5):
    """Create CNN model for ECG classification"""
    model = keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(512, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    return model

def create_mri_model(num_classes=5):
    """Create CNN model for MRI classification"""
    model = keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(512, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    return model

def load_and_preprocess_data(data_dir, img_size=(128, 128)):
    """Load and preprocess image data"""
    images = []
    labels = []
    class_names = sorted(os.listdir(data_dir))
    
    print(f"Loading data from: {data_dir}")
    print(f"Classes found: {class_names}")
    
    for class_idx, class_name in enumerate(class_names):
        class_dir = os.path.join(data_dir, class_name)
        if not os.path.isdir(class_dir):
            continue
            
        print(f"Loading {class_name}...")
        for img_name in os.listdir(class_dir):
            img_path = os.path.join(class_dir, img_name)
            try:
                img = Image.open(img_path)
                img = img.convert('RGB')  # Ensure RGB format
                img = img.resize(img_size)
                img_array = np.array(img)
                images.append(img_array)
                labels.append(class_idx)
            except Exception as e:
                print(f"Skipping {img_path}: {e}")
    
    images = np.array(images, dtype=np.float32)
    labels = np.array(labels)
    
    # Normalize pixel values
    images = images / 255.0
    
    print(f"Loaded {len(images)} images")
    return images, labels, class_names

def train_ecg_model():
    """Train ECG model"""
    print("=" * 60)
    print("Training ECG Model (5 Disease Classes)")
    print("=" * 60)
    
    # Check if dataset exists
    train_dir = "datasets/ecg/train"
    val_dir = "datasets/ecg/validation"
    
    if not os.path.exists(train_dir) or not os.path.exists(val_dir):
        print("❌ ECG dataset not found!")
        print("Please organize your dataset first.")
        return None
    
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # Load data
    print("Loading training data...")
    train_images, train_labels, class_names = load_and_preprocess_data(train_dir)
    
    print("Loading validation data...")
    val_images, val_labels, _ = load_and_preprocess_data(val_dir)
    
    # Convert labels to categorical
    num_classes = len(class_names)
    train_labels = keras.utils.to_categorical(train_labels, num_classes)
    val_labels = keras.utils.to_categorical(val_labels, num_classes)
    
    # Create model
    model = create_ecg_model(num_classes)
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Display model summary
    model.summary()
    
    # Train model
    print("Starting training...")
    history = model.fit(
        train_images, train_labels,
        epochs=50,
        batch_size=32,
        validation_data=(val_images, val_labels),
        verbose=1
    )
    
    # Save model
    model_path = "models/ecg_model.h5"
    model.save(model_path)
    print(f"✅ ECG model saved to: {model_path}")
    
    # Save class names
    with open("models/ecg_classes.json", "w") as f:
        json.dump(class_names, f)
    print(f"✅ ECG classes saved to: models/ecg_classes.json")
    
    return model

def train_mri_model():
    """Train MRI model"""
    print("=" * 60)
    print("Training MRI Model (5 Disease Classes)")
    print("=" * 60)
    
    # Check if dataset exists
    train_dir = "datasets/mri/train"
    val_dir = "datasets/mri/validation"
    
    if not os.path.exists(train_dir) or not os.path.exists(val_dir):
        print("❌ MRI dataset not found!")
        print("Please organize your dataset first.")
        return None
    
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # Load data
    print("Loading training data...")
    train_images, train_labels, class_names = load_and_preprocess_data(train_dir)
    
    print("Loading validation data...")
    val_images, val_labels, _ = load_and_preprocess_data(val_dir)
    
    # Convert labels to categorical
    num_classes = len(class_names)
    train_labels = keras.utils.to_categorical(train_labels, num_classes)
    val_labels = keras.utils.to_categorical(val_labels, num_classes)
    
    # Create model
    model = create_mri_model(num_classes)
    
    # Compile model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Display model summary
    model.summary()
    
    # Train model
    print("Starting training...")
    history = model.fit(
        train_images, train_labels,
        epochs=50,
        batch_size=32,
        validation_data=(val_images, val_labels),
        verbose=1
    )
    
    # Save model
    model_path = "models/mri_model.h5"
    model.save(model_path)
    print(f"✅ MRI model saved to: {model_path}")
    
    # Save class names
    with open("models/mri_classes.json", "w") as f:
        json.dump(class_names, f)
    print(f"✅ MRI classes saved to: models/mri_classes.json")
    
    return model

def main():
    """Main training function"""
    print("=" * 60)
    print("REAL AI MODEL TRAINER - Heart Disease Analyzer")
    print("=" * 60)
    
    # Check TensorFlow
    print(f"TensorFlow version: {tf.__version__}")
    
    # Check if GPU is available
    print(f"GPU available: {tf.config.list_physical_devices('GPU')}")
    
    # Train models
    print("\n[STEP 1] Training ECG model...")
    ecg_model = train_ecg_model()
    
    print("\n[STEP 2] Training MRI model...")
    mri_model = train_mri_model()
    
    print("\n" + "=" * 60)
    if ecg_model is not None and mri_model is not None:
        print("✅ ALL MODELS TRAINED SUCCESSFULLY!")
        print("You can now run the website with real AI predictions.")
        print("\nTo start the website:")
        print("  python app.py")
        print("\nAccess at: http://localhost:5000")
    else:
        print("⚠️  Some models failed to train.")
        print("Check the error messages above.")
    print("=" * 60)

if __name__ == "__main__":
    main()