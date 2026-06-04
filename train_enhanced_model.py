"""
Enhanced AI Model Trainer for Heart Disease Analyzer
Trains improved CNN models for ECG and MRI image classification with higher accuracy
"""

import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import numpy as np
from PIL import Image
import json
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def create_enhanced_ecg_model(num_classes=5):
    """Create enhanced CNN model for ECG classification with improved accuracy"""
    model = keras.Sequential([
        # First convolutional block
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Second convolutional block
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Third convolutional block
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Fourth convolutional block
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Dense layers with regularization
        layers.Flatten(),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    return model

def create_enhanced_mri_model(num_classes=5):
    """Create enhanced CNN model for MRI classification with improved accuracy"""
    model = keras.Sequential([
        # First convolutional block
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Second convolutional block
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Third convolutional block
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Fourth convolutional block
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Fifth convolutional block
        layers.Conv2D(512, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(512, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Dense layers with regularization
        layers.Flatten(),
        layers.Dense(1024, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
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

def create_data_generators(train_dir, val_dir, img_size=(128, 128), batch_size=32):
    """Create data generators with augmentation for training"""
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        vertical_flip=False,
        fill_mode='nearest'
    )
    
    # Only rescaling for validation
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical'
    )
    
    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical'
    )
    
    return train_generator, val_generator

def train_enhanced_ecg_model():
    """Train enhanced ECG model with improved accuracy"""
    print("=" * 60)
    print("Training Enhanced ECG Model (5 Disease Classes)")
    print("=" * 60)
    
    # Check if dataset exists
    train_dir = "datasets/varun_ecg/train"
    val_dir = "datasets/varun_ecg/val"
    
    if not os.path.exists(train_dir) or not os.path.exists(val_dir):
        print("❌ ECG dataset not found!")
        print("Please organize your dataset first.")
        return None
    
    # Check if directories have images
    train_count = sum([len(files) for r, d, files in os.walk(train_dir)])
    val_count = sum([len(files) for r, d, files in os.walk(val_dir)])
    
    if train_count == 0 or val_count == 0:
        print("❌ No images found in dataset directories!")
        print("Please add ECG images to your dataset folders:")
        print(f"  Training: {train_dir}")
        print(f"  Validation: {val_dir}")
        return None
    
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # Get class names
    class_names = sorted(os.listdir(train_dir))
    num_classes = len(class_names)
    print(f"Classes: {class_names}")
    
    # Create data generators
    print("Creating data generators with augmentation...")
    train_generator, val_generator = create_data_generators(train_dir, val_dir)
    
    # Create enhanced model
    model = create_enhanced_ecg_model(num_classes)
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Display model summary
    model.summary()
    
    # Callbacks for better training
    callbacks = [
        EarlyStopping(patience=15, restore_best_weights=True),
        ReduceLROnPlateau(factor=0.5, patience=10, min_lr=1e-7),
        ModelCheckpoint('models/best_ecg_model.h5', save_best_only=True)
    ]
    
    # Train model
    print("Starting enhanced training...")
    history = model.fit(
        train_generator,
        epochs=100,
        validation_data=val_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final model
    model_path = "models/enhanced_ecg_model.h5"
    model.save(model_path)
    print(f"✅ Enhanced ECG model saved to: {model_path}")
    
    # Save class names
    with open("models/ecg_classes.json", "w") as f:
        json.dump(class_names, f)
    print(f"✅ ECG classes saved to: models/ecg_classes.json")
    
    # Plot training history
    plot_training_history(history, "ECG_Model_Training_History.png")
    
    return model

def train_enhanced_mri_model():
    """Train enhanced MRI model with improved accuracy"""
    print("=" * 60)
    print("Training Enhanced MRI Model (5 Disease Classes)")
    print("=" * 60)
    
    # Check if dataset exists
    train_dir = "datasets/varun_mri/train"
    val_dir = "datasets/varun_mri/val"
    
    if not os.path.exists(train_dir) or not os.path.exists(val_dir):
        print("❌ MRI dataset not found!")
        print("Please organize your dataset first.")
        return None
    
    # Check if directories have images
    train_count = sum([len(files) for r, d, files in os.walk(train_dir)])
    val_count = sum([len(files) for r, d, files in os.walk(val_dir)])
    
    if train_count == 0 or val_count == 0:
        print("❌ No images found in dataset directories!")
        print("Please add MRI images to your dataset folders:")
        print(f"  Training: {train_dir}")
        print(f"  Validation: {val_dir}")
        return None
    
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # Get class names
    class_names = sorted(os.listdir(train_dir))
    num_classes = len(class_names)
    print(f"Classes: {class_names}")
    
    # Create data generators
    print("Creating data generators with augmentation...")
    train_generator, val_generator = create_data_generators(train_dir, val_dir)
    
    # Create enhanced model
    model = create_enhanced_mri_model(num_classes)
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Display model summary
    model.summary()
    
    # Callbacks for better training
    callbacks = [
        EarlyStopping(patience=15, restore_best_weights=True),
        ReduceLROnPlateau(factor=0.5, patience=10, min_lr=1e-7),
        ModelCheckpoint('models/best_mri_model.h5', save_best_only=True)
    ]
    
    # Train model
    print("Starting enhanced training...")
    history = model.fit(
        train_generator,
        epochs=100,
        validation_data=val_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final model
    model_path = "models/enhanced_mri_model.h5"
    model.save(model_path)
    print(f"✅ Enhanced MRI model saved to: {model_path}")
    
    # Save class names
    with open("models/mri_classes.json", "w") as f:
        json.dump(class_names, f)
    print(f"✅ MRI classes saved to: models/mri_classes.json")
    
    # Plot training history
    plot_training_history(history, "MRI_Model_Training_History.png")
    
    return model

def plot_training_history(history, filename):
    """Plot training history"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Plot accuracy
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    
    # Plot loss
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"✅ Training history plot saved to: {filename}")

def main():
    """Main training function"""
    print("Enhanced Heart Disease Analyzer Model Trainer")
    print("=" * 50)
    
    choice = input("What would you like to train?\n1. ECG Model\n2. MRI Model\n3. Both\nEnter choice (1/2/3): ")
    
    if choice == "1":
        train_enhanced_ecg_model()
    elif choice == "2":
        train_enhanced_mri_model()
    elif choice == "3":
        train_enhanced_ecg_model()
        train_enhanced_mri_model()
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()