import numpy as np
import gzip
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from utils import download_data_from_s3

def load_mnist_images(image_file):
    with gzip.open(image_file, 'rb') as f:
        f.read(16)  # Skip the header
        buf = f.read()
    image_size = 28
    num_images = len(buf) // (image_size * image_size)
    data = np.frombuffer(buf, dtype=np.uint8).astype(np.float32)
    images = data.reshape(num_images, image_size, image_size, 1)
    return images

def load_mnist_labels(label_file):
    with gzip.open(label_file, 'rb') as f:
        f.read(8)  # Skip the header
        buf = f.read()
    labels = np.frombuffer(buf, dtype=np.uint8)
    return labels

def preprocess_data(local_folder):
    X_train = load_mnist_images(os.path.join(local_folder, 'train-images-idx3-ubyte.gz'))
    y_train = load_mnist_labels(os.path.join(local_folder, 'train-labels-idx1-ubyte.gz'))
    X_test = load_mnist_images(os.path.join(local_folder, 't10k-images-idx3-ubyte.gz'))
    y_test = load_mnist_labels(os.path.join(local_folder, 't10k-labels-idx1-ubyte.gz'))

    # Normalize pixel values
    X_train = X_train / 255.0
    X_test = X_test / 255.0

    # Split training data into train and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

    return X_train, X_val, y_train, y_val, X_test, y_test
