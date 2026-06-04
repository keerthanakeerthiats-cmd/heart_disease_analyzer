"""
Advanced Image Preprocessing for Medical Images
Implements state-of-the-art preprocessing techniques to enhance image quality for better model accuracy
"""

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage import exposure, filters, restoration
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array


class AdvancedImageProcessor:
    """
    Advanced image preprocessing pipeline specifically designed for medical images
    """
    
    def __init__(self):
        pass
    
    def enhance_ecg_image(self, image_array):
        """
        Advanced ECG image enhancement using multiple techniques
        """
        # Ensure input is in the right format
        if len(image_array.shape) == 4:  # Batch dimension
            img = (image_array[0] * 255).astype(np.uint8)
        else:
            img = (image_array * 255).astype(np.uint8)
        
        # Convert to grayscale if needed
        if len(img.shape) == 3 and img.shape[-1] == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            gray = img if len(img.shape) == 2 else img[:, :, 0]
        
        # 1. Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # 2. Noise reduction with bilateral filter (preserves edges)
        denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)
        
        # 3. Contrast enhancement using histogram equalization
        eq = cv2.equalizeHist(denoised)
        
        # 4. Morphological operations to clean up the image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        cleaned = cv2.morphologyEx(eq, cv2.MORPH_CLOSE, kernel)
        
        # 5. Edge enhancement using unsharp masking
        gaussian = cv2.GaussianBlur(cleaned, (0, 0), 1.0)
        sharpened = cv2.addWeighted(cleaned, 1.5, gaussian, -0.5, 0)
        
        # 6. Gamma correction for brightness adjustment
        gamma = 1.2
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        gamma_corrected = cv2.LUT(sharpened, table)
        
        # Convert back to RGB format
        enhanced_rgb = cv2.cvtColor(gamma_corrected, cv2.COLOR_GRAY2RGB)
        
        # Normalize and add batch dimension
        enhanced_rgb = enhanced_rgb.astype(np.float32) / 255.0
        if len(image_array.shape) == 4:
            return np.expand_dims(enhanced_rgb, axis=0)
        else:
            return np.expand_dims(enhanced_rgb, axis=0)
    
    def enhance_mri_image(self, image_array):
        """
        Advanced MRI image enhancement using multiple techniques
        """
        # Ensure input is in the right format
        if len(image_array.shape) == 4:  # Batch dimension
            img = (image_array[0] * 255).astype(np.uint8)
        else:
            img = (image_array * 255).astype(np.uint8)
        
        # Convert to grayscale if needed
        if len(img.shape) == 3 and img.shape[-1] == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        else:
            gray = img if len(img.shape) == 2 else img[:, :, 0]
        
        # 1. Apply aggressive CLAHE for MRI images
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # 2. Noise reduction with non-local means (better for MRI)
        denoised = cv2.fastNlMeansDenoising(enhanced, None, 15, 7, 21)
        
        # 3. Advanced denoising with Wiener filtering
        denoised_wiener = restoration.wiener(denoised.astype(float), (5, 5)).astype(np.uint8)
        
        # 4. Contrast enhancement using adaptive histogram equalization
        adaptive_eq = exposure.equalize_adapthist(denoised_wiener, clip_limit=0.03)
        adaptive_eq = (adaptive_eq * 255).astype(np.uint8)
        
        # 5. Edge enhancement using Laplacian
        laplacian = cv2.Laplacian(adaptive_eq, cv2.CV_64F)
        laplacian = np.uint8(np.absolute(laplacian))
        enhanced_edges = cv2.addWeighted(adaptive_eq, 1.5, laplacian, -0.5, 0)
        
        # 6. Final bilateral filtering to smooth while preserving edges
        final = cv2.bilateralFilter(enhanced_edges, 15, 80, 80)
        
        # Convert back to RGB format
        enhanced_rgb = cv2.cvtColor(final, cv2.COLOR_GRAY2RGB)
        
        # Normalize and add batch dimension
        enhanced_rgb = enhanced_rgb.astype(np.float32) / 255.0
        if len(image_array.shape) == 4:
            return np.expand_dims(enhanced_rgb, axis=0)
        else:
            return np.expand_dims(enhanced_rgb, axis=0)
    
    def preprocess_for_model(self, image_path_or_array, target_size=(128, 128), modality='general'):
        """
        Complete preprocessing pipeline for medical images
        """
        # Load image if it's a path
        if isinstance(image_path_or_array, str):
            image = Image.open(image_path_or_array)
        else:
            image = Image.fromarray((image_path_or_array * 255).astype(np.uint8))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image
        image = image.resize(target_size)
        
        # Convert to array
        img_array = np.array(image, dtype=np.float32)
        
        # Normalize
        img_array = img_array / 255.0
        
        # Apply modality-specific enhancement
        if modality.lower() == 'ecg':
            enhanced = self.enhance_ecg_image(np.expand_dims(img_array, axis=0))
            return enhanced[0]  # Remove batch dimension for single image
        elif modality.lower() == 'mri':
            enhanced = self.enhance_mri_image(np.expand_dims(img_array, axis=0))
            return enhanced[0]  # Remove batch dimension for single image
        else:
            # Return normalized image without enhancement
            return img_array
    
    def batch_preprocess(self, image_list, target_size=(128, 128), modality='general'):
        """
        Preprocess a batch of images
        """
        processed_images = []
        for img in image_list:
            processed = self.preprocess_for_model(img, target_size, modality)
            processed_images.append(processed)
        
        return np.array(processed_images)


def create_advanced_augmentation_pipeline():
    """
    Create advanced augmentation pipeline specifically for medical images
    """
    def augment_medical_image(image, modality='general'):
        """
        Apply advanced augmentations suitable for medical images
        """
        # Random rotation (limited to avoid anatomical misinterpretation)
        if np.random.random() > 0.5:
            angle = np.random.uniform(-15, 15)  # Small rotations to preserve anatomy
            image = ndimage.rotate(image, angle, reshape=False, mode='nearest')
        
        # Random horizontal flip (anatomically appropriate for some modalities)
        if np.random.random() > 0.7 and modality in ['ecg', 'general']:
            image = np.fliplr(image)
        
        # Random brightness adjustment
        if np.random.random() > 0.5:
            factor = np.random.uniform(0.8, 1.2)
            image = np.clip(image * factor, 0, 1)
        
        # Random contrast adjustment
        if np.random.random() > 0.5:
            mean = np.mean(image)
            image = (image - mean) * np.random.uniform(0.8, 1.2) + mean
            image = np.clip(image, 0, 1)
        
        # Add small amount of Gaussian noise
        if np.random.random() > 0.7:
            noise = np.random.normal(0, 0.01, image.shape)
            image = np.clip(image + noise, 0, 1)
        
        return image
    
    return augment_medical_image


class MedicalImageAugmenter:
    """
    Advanced augmentation class specifically for medical images
    """
    
    def __init__(self, modality='general'):
        self.modality = modality
        self.augment_func = create_advanced_augmentation_pipeline()
    
    def augment(self, image_batch):
        """
        Apply augmentations to a batch of images
        """
        augmented_batch = []
        for img in image_batch:
            augmented_img = self.augment_func(img, self.modality)
            augmented_batch.append(augmented_img)
        
        return np.array(augmented_batch)


def apply_advanced_preprocessing(image_path, modality='ecg', enhance=True):
    """
    Convenience function to apply advanced preprocessing to a single image
    """
    processor = AdvancedImageProcessor()
    
    if enhance:
        if modality.lower() == 'ecg':
            # Load and preprocess for enhancement
            img = Image.open(image_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img_array = np.array(img.resize((128, 128)))
            img_array = img_array.astype(np.float32) / 255.0
            enhanced = processor.enhance_ecg_image(np.expand_dims(img_array, axis=0))
            return enhanced[0]
        elif modality.lower() == 'mri':
            # Load and preprocess for enhancement
            img = Image.open(image_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img_array = np.array(img.resize((128, 128)))
            img_array = img_array.astype(np.float32) / 255.0
            enhanced = processor.enhance_mri_image(np.expand_dims(img_array, axis=0))
            return enhanced[0]
    
    # Just basic preprocessing without enhancement
    return processor.preprocess_for_model(image_path, modality=modality)


# Example usage and testing functions
def test_preprocessing():
    """
    Test function to demonstrate the preprocessing capabilities
    """
    print("Testing Advanced Image Preprocessing...")
    
    # Create sample image for testing
    sample_img = np.random.rand(128, 128, 3).astype(np.float32)
    
    processor = AdvancedImageProcessor()
    
    # Test ECG enhancement
    enhanced_ecg = processor.enhance_ecg_image(sample_img)
    print(f"ECG enhancement completed. Output shape: {enhanced_ecg.shape}")
    
    # Test MRI enhancement
    enhanced_mri = processor.enhance_mri_image(sample_img)
    print(f"MRI enhancement completed. Output shape: {enhanced_mri.shape}")
    
    print("Advanced preprocessing test completed!")


if __name__ == "__main__":
    test_preprocessing()