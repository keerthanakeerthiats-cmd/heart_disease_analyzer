"""
Test TensorFlow installation
"""

try:
    import tensorflow as tf
    print("TensorFlow version:", tf.__version__)
    print("GPU available:", tf.config.list_physical_devices('GPU'))
    print("TensorFlow imported successfully!")
except Exception as e:
    print("Error importing TensorFlow:", str(e))
    print("Type of error:", type(e).__name__)