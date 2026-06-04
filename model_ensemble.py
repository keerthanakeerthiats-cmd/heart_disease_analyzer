"""
Model Ensemble for Heart Disease Detection
Implements ensemble methods to combine multiple models for improved accuracy
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import json
from sklearn.metrics import accuracy_score


class ModelEnsemble:
    """
    Ensemble of multiple models to improve prediction accuracy
    """
    
    def __init__(self, model_paths=None, weights=None):
        """
        Initialize ensemble with model paths
        
        Args:
            model_paths: List of paths to model files
            weights: List of weights for each model (optional, defaults to equal weights)
        """
        self.models = []
        self.weights = weights
        self.model_paths = model_paths or []
        
        # Load models
        for path in self.model_paths:
            if os.path.exists(path):
                model = keras.models.load_model(path)
                self.models.append(model)
                print(f"✅ Loaded model: {path}")
            else:
                print(f"❌ Model not found: {path}")
        
        if self.weights is None:
            # Equal weights if not specified
            self.weights = [1.0 / len(self.models)] * len(self.models)
    
    def predict(self, x):
        """
        Make prediction using ensemble of models
        
        Args:
            x: Input data
            
        Returns:
            Combined prediction from all models
        """
        if not self.models:
            raise ValueError("No models loaded for ensemble prediction")
        
        # Get predictions from all models
        predictions = []
        for i, model in enumerate(self.models):
            pred = model.predict(x)
            # Apply weight to this model's prediction
            weighted_pred = pred * self.weights[i]
            predictions.append(weighted_pred)
        
        # Sum weighted predictions
        combined_prediction = np.sum(predictions, axis=0)
        
        # Normalize to ensure probabilities sum to 1
        # (in case of weighted ensemble)
        combined_prediction = combined_prediction / np.sum(self.weights)
        
        return combined_prediction
    
    def predict_with_confidence(self, x):
        """
        Make prediction with confidence estimation based on model agreement
        
        Args:
            x: Input data
            
        Returns:
            Dictionary with prediction, confidence, and individual model predictions
        """
        if not self.models:
            raise ValueError("No models loaded for ensemble prediction")
        
        # Get predictions from all models
        individual_predictions = []
        for model in self.models:
            pred = model.predict(x)
            individual_predictions.append(pred)
        
        # Calculate ensemble prediction (weighted average)
        weighted_predictions = []
        for i, pred in enumerate(individual_predictions):
            weighted_pred = pred * self.weights[i]
            weighted_predictions.append(weighted_pred)
        
        ensemble_prediction = np.sum(weighted_predictions, axis=0) / np.sum(self.weights)
        
        # Calculate confidence based on agreement between models
        # Convert predictions to class predictions
        individual_classes = [np.argmax(pred, axis=1) for pred in individual_predictions]
        ensemble_class = np.argmax(ensemble_prediction, axis=1)
        
        # Calculate agreement percentage
        agreement = []
        for i in range(len(x)):
            model_classes = [pred[i] for pred in individual_classes]
            agreement_pct = sum(1 for cls in model_classes if cls == ensemble_class[i]) / len(self.models)
            agreement.append(agreement_pct)
        
        avg_agreement = np.mean(agreement) * 100
        
        return {
            'ensemble_prediction': ensemble_prediction,
            'individual_predictions': individual_predictions,
            'confidence': avg_agreement,
            'agreement': agreement
        }


class AdvancedEnsemblePredictor:
    """
    Advanced ensemble predictor with multiple strategies
    """
    
    def __init__(self, model_paths_dict):
        """
        Initialize with different model types
        
        Args:
            model_paths_dict: Dictionary with keys like 'ecg_basic', 'ecg_advanced', etc.
        """
        self.ensemble_predictors = {}
        
        # Group models by type
        for model_type, paths in model_paths_dict.items():
            self.ensemble_predictors[model_type] = ModelEnsemble(paths)
    
    def predict_ecg(self, x):
        """Predict using ECG model ensemble"""
        ecg_keys = [key for key in self.ensemble_predictors.keys() if 'ecg' in key.lower()]
        if not ecg_keys:
            raise ValueError("No ECG models available")
        
        # Average predictions from all ECG models
        all_predictions = []
        for key in ecg_keys:
            pred = self.ensemble_predictors[key].predict(x)
            all_predictions.append(pred)
        
        return np.mean(all_predictions, axis=0)
    
    def predict_mri(self, x):
        """Predict using MRI model ensemble"""
        mri_keys = [key for key in self.ensemble_predictors.keys() if 'mri' in key.lower()]
        if not mri_keys:
            raise ValueError("No MRI models available")
        
        # Average predictions from all MRI models
        all_predictions = []
        for key in mri_keys:
            pred = self.ensemble_predictors[key].predict(x)
            all_predictions.append(pred)
        
        return np.mean(all_predictions, axis=0)


class StackingEnsemble:
    """
    Stacking ensemble that uses a meta-learner to combine base model predictions
    """
    
    def __init__(self, base_models, meta_learner=None):
        """
        Initialize stacking ensemble
        
        Args:
            base_models: List of base models
            meta_learner: Meta-learner model (if None, uses simple averaging)
        """
        self.base_models = base_models
        self.meta_learner = meta_learner
        self.is_fitted = False
    
    def fit_meta_learner(self, X_val, y_val):
        """
        Fit the meta-learner using validation data
        """
        if self.meta_learner is None:
            # If no meta-learner provided, just use averaging
            self.is_fitted = True
            return
        
        # Get base model predictions on validation set
        base_predictions = []
        for model in self.base_models:
            pred = model.predict(X_val)
            base_predictions.append(pred)
        
        # Stack predictions (shape: samples x (classes * num_models))
        stacked_predictions = np.concatenate(base_predictions, axis=1)
        
        # Fit meta-learner
        self.meta_learner.fit(stacked_predictions, y_val)
        self.is_fitted = True
    
    def predict(self, x):
        """
        Make prediction using stacking ensemble
        """
        if not self.is_fitted:
            # If meta-learner not fitted, use simple averaging
            base_predictions = []
            for model in self.base_models:
                pred = model.predict(x)
                base_predictions.append(pred)
            return np.mean(base_predictions, axis=0)
        
        # Get base model predictions
        base_predictions = []
        for model in self.base_models:
            pred = model.predict(x)
            base_predictions.append(pred)
        
        # Stack predictions
        stacked_predictions = np.concatenate(base_predictions, axis=1)
        
        # Use meta-learner to make final prediction
        return self.meta_learner.predict(stacked_predictions)


def create_optimized_ensemble(model_type='ecg'):
    """
    Create an optimized ensemble for a specific model type
    """
    model_paths = []
    
    if model_type.lower() == 'ecg':
        # Look for various ECG models
        possible_paths = [
            'models/ecg_model.h5',
            'models/enhanced_ecg_model.h5',
            'models/best_ecg_model.h5',
            'models/advanced_ecg_model.h5'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                model_paths.append(path)
    
    elif model_type.lower() == 'mri':
        # Look for various MRI models
        possible_paths = [
            'models/mri_model.h5',
            'models/enhanced_mri_model.h5',
            'models/best_mri_model.h5',
            'models/advanced_mri_model.h5'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                model_paths.append(path)
    
    if not model_paths:
        print(f"No {model_type} models found for ensemble")
        return None
    
    # Create ensemble with equal weights
    ensemble = ModelEnsemble(model_paths)
    return ensemble


def load_ensemble_class_names(model_type='ecg'):
    """
    Load class names for ensemble models
    """
    # Try different possible class name files
    possible_paths = [
        f'models/{model_type}_classes.json',
        f'models/advanced_{model_type}_classes.json',
        f'models/enhanced_{model_type}_classes.json'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
    
    # Default class names if no file found
    if model_type.lower() == 'ecg':
        return ['Normal', 'Myocardial Infarction', 'Abnormal Heartbeat', 'History of MI', 'Arrhythmia']
    elif model_type.lower() == 'mri':
        return ['Normal', 'Cardiomyopathy', 'Coronary Artery Disease', 'Heart Failure', 'Myocardial Infarction']
    
    return []


def get_model_accuracy_estimation(model_path, X_test, y_test):
    """
    Estimate model accuracy on test data (for weighting purposes)
    """
    if not os.path.exists(model_path):
        return 0.0
    
    try:
        model = keras.models.load_model(model_path)
        predictions = model.predict(X_test)
        predicted_classes = np.argmax(predictions, axis=1)
        true_classes = np.argmax(y_test, axis=1) if y_test.ndim > 1 else y_test
        accuracy = accuracy_score(true_classes, predicted_classes)
        return accuracy
    except:
        return 0.0


def create_weighted_ensemble_by_accuracy(model_type='ecg', X_test=None, y_test=None):
    """
    Create ensemble with weights based on model accuracy
    """
    model_paths = []
    
    if model_type.lower() == 'ecg':
        possible_paths = [
            'models/ecg_model.h5',
            'models/enhanced_ecg_model.h5',
            'models/best_ecg_model.h5',
            'models/advanced_ecg_model.h5'
        ]
    elif model_type.lower() == 'mri':
        possible_paths = [
            'models/mri_model.h5',
            'models/enhanced_mri_model.h5',
            'models/best_mri_model.h5',
            'models/advanced_mri_model.h5'
        ]
    else:
        return None
    
    # Filter to only existing models
    available_paths = [path for path in possible_paths if os.path.exists(path)]
    
    if not available_paths:
        print(f"No {model_type} models found for ensemble")
        return None
    
    # Calculate accuracies if test data provided
    if X_test is not None and y_test is not None:
        accuracies = []
        for path in available_paths:
            acc = get_model_accuracy_estimation(path, X_test, y_test)
            accuracies.append(acc)
        
        # Convert accuracies to weights (higher accuracy = higher weight)
        total_acc = sum(accuracies)
        if total_acc > 0:
            weights = [acc / total_acc for acc in accuracies]
        else:
            # Equal weights if no accuracy data
            weights = [1.0 / len(available_paths)] * len(available_paths)
    else:
        # Equal weights if no test data
        weights = [1.0 / len(available_paths)] * len(available_paths)
    
    # Create ensemble
    ensemble = ModelEnsemble(available_paths, weights=weights)
    return ensemble


# Example usage
def example_usage():
    """
    Example of how to use the ensemble system
    """
    print("Creating model ensembles...")
    
    # Create ECG ensemble
    ecg_ensemble = create_optimized_ensemble('ecg')
    if ecg_ensemble:
        print(f"ECG ensemble created with {len(ecg_ensemble.models)} models")
        ecg_classes = load_ensemble_class_names('ecg')
        print(f"ECG classes: {ecg_classes}")
    
    # Create MRI ensemble
    mri_ensemble = create_optimized_ensemble('mri')
    if mri_ensemble:
        print(f"MRI ensemble created with {len(mri_ensemble.models)} models")
        mri_classes = load_ensemble_class_names('mri')
        print(f"MRI classes: {mri_classes}")
    
    print("Ensemble system ready!")


if __name__ == "__main__":
    example_usage()