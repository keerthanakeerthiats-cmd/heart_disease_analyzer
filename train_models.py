"""
Training script for ECG and MRI heart disease detection models
This script demonstrates how to train the models with your own datasets
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt

# Import model architectures from app.py
import sys
sys.path.append(os.path.dirname(__file__))
from app import create_ecg_model, create_mri_model

def train_ecg_model(train_dir, val_dir, epochs=50, batch_size=32):
    """
    Train ECG classification model
    
    Dataset structure:
    train_dir/
        normal/
        myocardial_infarction/
        abnormal_heartbeat/
        history_of_mi/
        arrhythmia/
    """
    print("=" * 60)
    print("Training ECG Model (5 Disease Classes)")
    print("=" * 60)
    
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=False,
        fill_mode='nearest'
    )
    
    # Only rescaling for validation
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # Create data generators
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(128, 128),
        batch_size=batch_size,
        class_mode='categorical',
        classes=['normal', 'myocardial_infarction', 'abnormal_heartbeat', 
                'history_of_mi', 'arrhythmia']
    )
    
    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(128, 128),
        batch_size=batch_size,
        class_mode='categorical',
        classes=['normal', 'myocardial_infarction', 'abnormal_heartbeat', 
                'history_of_mi', 'arrhythmia']
    )
    
    # Create model with 5 classes
    model = create_ecg_model(num_classes=5)
    
    # Print model summary
    model.summary()
    
    # Callbacks
    callbacks = [
        ModelCheckpoint(
            'models/ecg_model_best.h5',
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # Train model
    history = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=val_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final model
    model.save('models/ecg_model.h5')
    print("\nECG Model saved to models/ecg_model.h5")
    
    # Plot training history
    plot_training_history(history, 'ECG')
    
    return model, history

def train_mri_model(train_dir, val_dir, epochs=50, batch_size=32):
    """
    Train MRI classification model
    
    Dataset structure:
    train_dir/
        normal/
        cardiomyopathy/
        coronary_artery_disease/
        heart_failure/
        myocardial_infarction/
    """
    print("\n" + "=" * 60)
    print("Training MRI Model (5 Disease Classes)")
    print("=" * 60)
    
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=15,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.15,
        zoom_range=0.15,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Only rescaling for validation
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # Create data generators
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(128, 128),
        batch_size=batch_size,
        class_mode='categorical',
        classes=['normal', 'cardiomyopathy', 'coronary_artery_disease',
                'heart_failure', 'myocardial_infarction']
    )
    
    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(128, 128),
        batch_size=batch_size,
        class_mode='categorical',
        classes=['normal', 'cardiomyopathy', 'coronary_artery_disease',
                'heart_failure', 'myocardial_infarction']
    )
    
    # Create model with 5 classes
    model = create_mri_model(num_classes=5)
    
    # Print model summary
    model.summary()
    
    # Callbacks
    callbacks = [
        ModelCheckpoint(
            'models/mri_model_best.h5',
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        )
    ]
    
    # Train model
    history = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=val_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save final model
    model.save('models/mri_model.h5')
    print("\nMRI Model saved to models/mri_model.h5")
    
    # Plot training history
    plot_training_history(history, 'MRI')
    
    return model, history

def plot_training_history(history, model_name):
    """Plot training and validation accuracy/loss"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Plot accuracy
    ax1.plot(history.history['accuracy'], label='Training Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Validation Accuracy')
    ax1.set_title(f'{model_name} Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True)
    
    # Plot loss
    ax2.plot(history.history['loss'], label='Training Loss')
    ax2.plot(history.history['val_loss'], label='Validation Loss')
    ax2.set_title(f'{model_name} Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(f'models/{model_name.lower()}_training_history.png')
    print(f"Training history plot saved to models/{model_name.lower()}_training_history.png")
    plt.close()

def create_sample_dataset_structure():
    """Create sample dataset directory structure"""
    directories = [
        'datasets/ecg/train/normal',
        'datasets/ecg/train/myocardial_infarction',
        'datasets/ecg/train/abnormal_heartbeat',
        'datasets/ecg/train/history_of_mi',
        'datasets/ecg/train/arrhythmia',
        'datasets/ecg/val/normal',
        'datasets/ecg/val/myocardial_infarction',
        'datasets/ecg/val/abnormal_heartbeat',
        'datasets/ecg/val/history_of_mi',
        'datasets/ecg/val/arrhythmia',
        'datasets/mri/train/normal',
        'datasets/mri/train/cardiomyopathy',
        'datasets/mri/train/coronary_artery_disease',
        'datasets/mri/train/heart_failure',
        'datasets/mri/train/myocardial_infarction',
        'datasets/mri/val/normal',
        'datasets/mri/val/cardiomyopathy',
        'datasets/mri/val/coronary_artery_disease',
        'datasets/mri/val/heart_failure',
        'datasets/mri/val/myocardial_infarction'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("Sample dataset structure created!")
    print("\nPlease organize your images in the following structure:")
    print("\ndatasets/")
    print("  ecg/")
    print("    train/")
    print("      normal/                    <- Normal ECG images")
    print("      myocardial_infarction/     <- MI ECG images")
    print("      abnormal_heartbeat/        <- Abnormal rhythm images")
    print("      history_of_mi/             <- History of MI images")
    print("      arrhythmia/                <- Arrhythmia images")
    print("    val/")
    print("      (same structure as train)")
    print("  mri/")
    print("    train/")
    print("      normal/                    <- Normal MRI images")
    print("      cardiomyopathy/            <- Cardiomyopathy MRI images")
    print("      coronary_artery_disease/   <- CAD MRI images")
    print("      heart_failure/             <- Heart failure MRI images")
    print("      myocardial_infarction/     <- MI MRI images")
    print("    val/")
    print("      (same structure as train)")

if __name__ == '__main__':
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    # Create sample dataset structure
    create_sample_dataset_structure()
    
    print("\n" + "=" * 60)
    print("DATASET PREPARATION")
    print("=" * 60)
    print("\nBefore training, please:")
    print("1. Download or collect ECG and MRI datasets")
    print("2. Organize images into the created directory structure")
    print("3. Ensure you have enough images (minimum 100-500 per class)")
    print("4. Split data into training and validation sets (80/20 split)")
    print("\nPopular datasets:")
    print("- ECG: MIT-BIH Arrhythmia Database, PTB Diagnostic ECG Database")
    print("- MRI: Cardiac Atlas Project, UK Biobank")
    
    print("\n" + "=" * 60)
    
    # Check if datasets exist
    ecg_train_exists = os.path.exists('datasets/ecg/train/normal') and \
                       os.path.exists('datasets/ecg/train/abnormal')
    ecg_val_exists = os.path.exists('datasets/ecg/val/normal') and \
                     os.path.exists('datasets/ecg/val/abnormal')
    
    mri_train_exists = os.path.exists('datasets/mri/train/normal') and \
                       os.path.exists('datasets/mri/train/disease')
    mri_val_exists = os.path.exists('datasets/mri/val/normal') and \
                     os.path.exists('datasets/mri/val/disease')
    
    # Check if there are images in the directories
    train_choice = input("\nDo you want to train the models now? (y/n): ").lower()
    
    if train_choice == 'y':
        if ecg_train_exists and ecg_val_exists:
            print("\nStarting ECG model training...")
            ecg_model, ecg_history = train_ecg_model(
                'datasets/ecg/train',
                'datasets/ecg/val',
                epochs=50,
                batch_size=32
            )
        else:
            print("\nECG dataset not found. Skipping ECG model training.")
        
        if mri_train_exists and mri_val_exists:
            print("\nStarting MRI model training...")
            mri_model, mri_history = train_mri_model(
                'datasets/mri/train',
                'datasets/mri/val',
                epochs=50,
                batch_size=32
            )
        else:
            print("\nMRI dataset not found. Skipping MRI model training.")
        
        print("\n" + "=" * 60)
        print("Training completed!")
        print("=" * 60)
        print("\nTrained models saved in the 'models/' directory")
        print("You can now run the web application with: python app.py")
    else:
        print("\nTraining skipped. Add your datasets and run this script again.")
