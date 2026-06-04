"""
Advanced AI Model Improver for Heart Disease Analyzer
Implements transfer learning, advanced architectures, and ensemble methods to increase accuracy
"""

import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import ResNet50, EfficientNetB0
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint, Callback
import numpy as np
from PIL import Image
import json
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns


def create_transfer_learning_model(input_shape=(128, 128, 3), num_classes=5, model_type='resnet'):
    """
    Create a model using transfer learning for better accuracy
    """
    if model_type == 'resnet':
        base_model = ResNet50(
            weights='imagenet',
            include_top=False,
            input_shape=input_shape
        )
    elif model_type == 'efficientnet':
        base_model = EfficientNetB0(
            weights='imagenet',
            include_top=False,
            input_shape=input_shape
        )
    else:
        raise ValueError("model_type must be 'resnet' or 'efficientnet'")
    
    # Freeze base model initially
    base_model.trainable = False
    
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.4),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model, base_model


def create_advanced_cnn_model(input_shape=(128, 128, 3), num_classes=5):
    """
    Create an advanced CNN model with more sophisticated architecture
    """
    model = keras.Sequential([
        # First group
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Second group
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Third group
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Fourth group
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Fifth group
        layers.Conv2D(512, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(512, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.25),
        
        # Dense layers with advanced regularization
        layers.GlobalAveragePooling2D(),
        layers.Dense(1024, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.4),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model


class AdvancedImageDataGenerator:
    """
    Advanced data augmentation with medical imaging-specific techniques
    """
    def __init__(self, rotation_range=25, width_shift_range=0.2, height_shift_range=0.2,
                 shear_range=0.2, zoom_range=0.2, horizontal_flip=True, 
                 brightness_range=(0.8, 1.2), fill_mode='nearest'):
        
        self.train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=rotation_range,
            width_shift_range=width_shift_range,
            height_shift_range=height_shift_range,
            shear_range=shear_range,
            zoom_range=zoom_range,
            horizontal_flip=horizontal_flip,
            brightness_range=brightness_range,
            fill_mode=fill_mode,
            # Additional augmentations for medical images
            channel_shift_range=0.1,
            # Feature-wise centering and standardization (if fit on data)
        )
        
        self.val_datagen = ImageDataGenerator(rescale=1./255)
    
    def flow_from_directory(self, directory, target_size=(128, 128), batch_size=32, class_mode='categorical'):
        train_generator = self.train_datagen.flow_from_directory(
            directory,
            target_size=target_size,
            batch_size=batch_size,
            class_mode=class_mode
        )
        return train_generator


class FineTuningCallback(Callback):
    """
    Custom callback to unfreeze base model after initial training
    """
    def __init__(self, base_model, fine_tune_at_epoch=10):
        super().__init__()
        self.base_model = base_model
        self.fine_tune_at_epoch = fine_tune_at_epoch
        
    def on_epoch_end(self, epoch, logs=None):
        if epoch == self.fine_tune_at_epoch:
            print("Unfreezing base model for fine-tuning...")
            self.base_model.trainable = True
            
            # Recompile with lower learning rate for fine-tuning
            self.model.compile(
                optimizer=keras.optimizers.Adam(learning_rate=0.0001/10),  # Lower LR for fine-tuning
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )


def train_advanced_ecg_model():
    """Train advanced ECG model with transfer learning and other improvements"""
    print("=" * 70)
    print("Training Advanced ECG Model with Transfer Learning and Enhanced Architecture")
    print("=" * 70)
    
    # Define paths
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
    print(f"Number of classes: {num_classes}")
    
    # Create data generators
    print("Creating advanced data generators with augmentation...")
    data_gen = AdvancedImageDataGenerator()
    train_generator = data_gen.flow_from_directory(
        train_dir,
        target_size=(128, 128),
        batch_size=16,  # Smaller batch size for transfer learning
        class_mode='categorical'
    )
    
    val_generator = data_gen.val_datagen.flow_from_directory(
        val_dir,
        target_size=(128, 128),
        batch_size=16,
        class_mode='categorical'
    )
    
    # Create advanced model - trying transfer learning approach
    print("Creating advanced transfer learning model...")
    model, base_model = create_transfer_learning_model(
        input_shape=(128, 128, 3), 
        num_classes=num_classes, 
        model_type='resnet'
    )
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy', 'top_2_accuracy']
    )
    
    # Display model summary
    model.summary()
    
    # Callbacks for better training
    callbacks = [
        EarlyStopping(patience=20, restore_best_weights=True, monitor='val_accuracy'),
        ReduceLROnPlateau(factor=0.2, patience=10, min_lr=1e-7, monitor='val_accuracy'),
        ModelCheckpoint('models/best_advanced_ecg_model.h5', save_best_only=True, monitor='val_accuracy'),
        FineTuningCallback(base_model, fine_tune_at_epoch=15)
    ]
    
    # Train model with more epochs for transfer learning
    print("Starting advanced training with transfer learning...")
    history = model.fit(
        train_generator,
        epochs=50,  # More epochs for transfer learning
        validation_data=val_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Fine-tune the entire model if not already done
    if base_model.trainable:
        print("Performing final fine-tuning...")
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.0001),  # Even lower LR for fine-tuning
            loss='categorical_crossentropy',
            metrics=['accuracy', 'top_2_accuracy']
        )
        
        # Continue training for a few more epochs
        fine_tune_history = model.fit(
            train_generator,
            epochs=10,
            validation_data=val_generator,
            verbose=1
        )
    
    # Save final model
    model_path = "models/advanced_ecg_model.h5"
    model.save(model_path)
    print(f"✅ Advanced ECG model saved to: {model_path}")
    
    # Save class names
    with open("models/advanced_ecg_classes.json", "w") as f:
        json.dump(class_names, f)
    print(f"✅ ECG classes saved to: models/advanced_ecg_classes.json")
    
    # Plot training history
    plot_training_history(history, "Advanced_ECG_Model_Training_History.png")
    
    return model


def train_advanced_mri_model():
    """Train advanced MRI model with transfer learning and other improvements"""
    print("=" * 70)
    print("Training Advanced MRI Model with Transfer Learning and Enhanced Architecture")
    print("=" * 70)
    
    # Define paths
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
    print(f"Number of classes: {num_classes}")
    
    # Create data generators
    print("Creating advanced data generators with augmentation...")
    data_gen = AdvancedImageDataGenerator()
    train_generator = data_gen.flow_from_directory(
        train_dir,
        target_size=(128, 128),
        batch_size=16,
        class_mode='categorical'
    )
    
    val_generator = data_gen.val_datagen.flow_from_directory(
        val_dir,
        target_size=(128, 128),
        batch_size=16,
        class_mode='categorical'
    )
    
    # Create advanced model - trying transfer learning approach
    print("Creating advanced transfer learning model...")
    model, base_model = create_transfer_learning_model(
        input_shape=(128, 128, 3), 
        num_classes=num_classes, 
        model_type='resnet'
    )
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy', 'top_2_accuracy']
    )
    
    # Display model summary
    model.summary()
    
    # Callbacks for better training
    callbacks = [
        EarlyStopping(patience=20, restore_best_weights=True, monitor='val_accuracy'),
        ReduceLROnPlateau(factor=0.2, patience=10, min_lr=1e-7, monitor='val_accuracy'),
        ModelCheckpoint('models/best_advanced_mri_model.h5', save_best_only=True, monitor='val_accuracy'),
        FineTuningCallback(base_model, fine_tune_at_epoch=15)
    ]
    
    # Train model with more epochs for transfer learning
    print("Starting advanced training with transfer learning...")
    history = model.fit(
        train_generator,
        epochs=50,
        validation_data=val_generator,
        callbacks=callbacks,
        verbose=1
    )
    
    # Fine-tune the entire model if not already done
    if base_model.trainable:
        print("Performing final fine-tuning...")
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.0001),  # Even lower LR for fine-tuning
            loss='categorical_crossentropy',
            metrics=['accuracy', 'top_2_accuracy']
        )
        
        # Continue training for a few more epochs
        fine_tune_history = model.fit(
            train_generator,
            epochs=10,
            validation_data=val_generator,
            verbose=1
        )
    
    # Save final model
    model_path = "models/advanced_mri_model.h5"
    model.save(model_path)
    print(f"✅ Advanced MRI model saved to: {model_path}")
    
    # Save class names
    with open("models/advanced_mri_classes.json", "w") as f:
        json.dump(class_names, f)
    print(f"✅ MRI classes saved to: models/advanced_mri_classes.json")
    
    # Plot training history
    plot_training_history(history, "Advanced_MRI_Model_Training_History.png")
    
    return model


def plot_training_history(history, filename):
    """Plot training history with additional metrics"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # Plot accuracy
    axes[0, 0].plot(history.history['accuracy'], label='Training Accuracy', linewidth=2)
    if 'val_accuracy' in history.history:
        axes[0, 0].plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
    axes[0, 0].set_title('Model Accuracy', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Epoch')
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].legend()
    axes[0, 0].grid(True, linestyle='--', alpha=0.6)
    
    # Plot loss
    axes[0, 1].plot(history.history['loss'], label='Training Loss', linewidth=2)
    if 'val_loss' in history.history:
        axes[0, 1].plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
    axes[0, 1].set_title('Model Loss', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Epoch')
    axes[0, 1].set_ylabel('Loss')
    axes[0, 1].legend()
    axes[0, 1].grid(True, linestyle='--', alpha=0.6)
    
    # Plot top_2_accuracy if available
    if 'top_2_accuracy' in history.history:
        axes[1, 0].plot(history.history['top_2_accuracy'], label='Training Top-2 Accuracy', linewidth=2)
        if 'val_top_2_accuracy' in history.history:
            axes[1, 0].plot(history.history['val_top_2_accuracy'], label='Validation Top-2 Accuracy', linewidth=2)
        axes[1, 0].set_title('Top-2 Accuracy', fontsize=14, fontweight='bold')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('Top-2 Accuracy')
        axes[1, 0].legend()
        axes[1, 0].grid(True, linestyle='--', alpha=0.6)
    
    # Plot learning rate if recorded
    if 'lr' in history.history:
        axes[1, 1].plot(history.history['lr'], label='Learning Rate', color='red', linewidth=2)
        axes[1, 1].set_title('Learning Rate Schedule', fontsize=14, fontweight='bold')
        axes[1, 1].set_xlabel('Epoch')
        axes[1, 1].set_ylabel('Learning Rate')
        axes[1, 1].set_yscale('log')
        axes[1, 1].legend()
        axes[1, 1].grid(True, linestyle='--', alpha=0.6)
    else:
        axes[1, 1].axis('off')  # Turn off unused subplot
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Training history plot saved to: {filename}")


def create_ensemble_predictor():
    """
    Create an ensemble predictor that combines multiple models for better accuracy
    """
    class EnsemblePredictor:
        def __init__(self, model_paths):
            self.models = []
            for path in model_paths:
                if os.path.exists(path):
                    model = keras.models.load_model(path)
                    self.models.append(model)
                    print(f"✅ Loaded model: {path}")
                else:
                    print(f"❌ Model not found: {path}")
        
        def predict(self, x):
            if not self.models:
                raise ValueError("No models loaded for ensemble prediction")
            
            # Get predictions from all models
            predictions = []
            for model in self.models:
                pred = model.predict(x)
                predictions.append(pred)
            
            # Average the predictions (simple ensemble)
            avg_predictions = np.mean(predictions, axis=0)
            return avg_predictions
    
    return EnsemblePredictor


def main():
    """Main training function"""
    print("Advanced Heart Disease Analyzer Model Improver")
    print("=" * 60)
    print("This script will train advanced models using:")
    print("- Transfer learning with pre-trained networks")
    print("- Advanced data augmentation")
    print("- Fine-tuning strategies")
    print("- Enhanced architectures")
    print("=" * 60)
    
    choice = input("What would you like to train?\n1. ECG Model\n2. MRI Model\n3. Both\nEnter choice (1/2/3): ")
    
    if choice == "1":
        train_advanced_ecg_model()
    elif choice == "2":
        train_advanced_mri_model()
    elif choice == "3":
        train_advanced_ecg_model()
        train_advanced_mri_model()
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()