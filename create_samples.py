"""
Create sample test images for ECG and MRI analysis
This generates synthetic test images for demonstration purposes
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os
import cv2

def create_sample_ecg_image(filename, is_normal=True):
    """Create a synthetic ECG-like image"""
    width, height = 800, 400
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw grid (typical ECG grid)
    grid_color = (255, 200, 200)
    for x in range(0, width, 20):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, 20):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)
    
    # Draw ECG waveform
    points = []
    baseline = height // 2
    
    for x in range(width):
        if is_normal:
            # Normal ECG pattern (PQRST waves)
            wave = 0
            x_norm = (x % 200) / 200
            
            # P wave
            if 0.1 < x_norm < 0.2:
                wave = 15 * np.sin((x_norm - 0.1) * np.pi / 0.1)
            # QRS complex
            elif 0.3 < x_norm < 0.38:
                if 0.32 < x_norm < 0.36:
                    wave = -100 * np.sin((x_norm - 0.32) * np.pi / 0.04)
                else:
                    wave = 20 * np.sin((x_norm - 0.3) * np.pi / 0.08)
            # T wave
            elif 0.5 < x_norm < 0.7:
                wave = 30 * np.sin((x_norm - 0.5) * np.pi / 0.2)
        else:
            # Abnormal ECG (irregular rhythm)
            wave = 30 * np.sin(x * 0.05) + 20 * np.sin(x * 0.1) + np.random.normal(0, 5)
            if x % 150 < 20:
                wave += 50 * np.sin((x % 150) * np.pi / 20)
        
        y = int(baseline - wave)
        points.append((x, y))
    
    # Draw the ECG line
    draw.line(points, fill='black', width=2)
    
    # Add label
    try:
        label = "Normal ECG" if is_normal else "Abnormal ECG"
        draw.text((10, 10), label, fill='blue')
    except:
        pass
    
    # Save image
    img.save(filename)
    print(f"Created: {filename}")

def create_sample_mri_image(filename, is_normal=True):
    """Create a synthetic MRI-like image of a heart"""
    size = 400
    img = np.zeros((size, size, 3), dtype=np.uint8)
    
    # Create background gradient (typical MRI appearance)
    for i in range(size):
        for j in range(size):
            intensity = 30 + int(20 * np.sin(i * 0.05) + 20 * np.cos(j * 0.05))
            img[i, j] = [intensity, intensity, intensity]
    
    # Draw heart-like shape
    center_x, center_y = size // 2, size // 2 - 20
    
    # Create heart chambers
    if is_normal:
        # Normal heart chambers
        cv2.ellipse(img, (center_x - 40, center_y), (50, 60), 0, 0, 360, (100, 100, 100), -1)
        cv2.ellipse(img, (center_x + 40, center_y), (50, 60), 0, 0, 360, (100, 100, 100), -1)
        cv2.ellipse(img, (center_x, center_y + 50), (70, 80), 0, 0, 360, (120, 120, 120), -1)
    else:
        # Abnormal heart (enlarged chambers)
        cv2.ellipse(img, (center_x - 40, center_y), (60, 70), 0, 0, 360, (100, 100, 100), -1)
        cv2.ellipse(img, (center_x + 50, center_y), (65, 75), 0, 0, 360, (100, 100, 100), -1)
        cv2.ellipse(img, (center_x, center_y + 55), (80, 90), 0, 0, 360, (120, 120, 120), -1)
        
        # Add irregular shapes to indicate disease
        cv2.circle(img, (center_x + 60, center_y - 20), 15, (150, 150, 150), -1)
    
    # Add some texture
    noise = np.random.normal(0, 10, (size, size, 3))
    img = np.clip(img + noise, 0, 255).astype(np.uint8)
    
    # Apply Gaussian blur for MRI-like appearance
    img = cv2.GaussianBlur(img, (5, 5), 0)
    
    # Add label
    label = "Normal MRI" if is_normal else "Disease MRI"
    cv2.putText(img, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Save image
    cv2.imwrite(filename, img)
    print(f"Created: {filename}")

def create_sample_images():
    """Create sample test images"""
    # Create sample_images directory
    os.makedirs('sample_images', exist_ok=True)
    
    print("Generating sample ECG images...")
    create_sample_ecg_image('sample_images/ecg_normal_1.png', is_normal=True)
    create_sample_ecg_image('sample_images/ecg_normal_2.png', is_normal=True)
    create_sample_ecg_image('sample_images/ecg_abnormal_1.png', is_normal=False)
    create_sample_ecg_image('sample_images/ecg_abnormal_2.png', is_normal=False)
    
    print("\nGenerating sample MRI images...")
    create_sample_mri_image('sample_images/mri_normal_1.png', is_normal=True)
    create_sample_mri_image('sample_images/mri_normal_2.png', is_normal=True)
    create_sample_mri_image('sample_images/mri_disease_1.png', is_normal=False)
    create_sample_mri_image('sample_images/mri_disease_2.png', is_normal=False)
    
    print("\n" + "=" * 60)
    print("Sample images created successfully!")
    print("=" * 60)
    print("\nYou can find them in the 'sample_images/' directory")
    print("\nThese images can be used to test the web application.")
    print("Upload them through the web interface after starting the app.")

if __name__ == '__main__':
    create_sample_images()
