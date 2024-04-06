import os
import numpy as np
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import load_img, img_to_array
from keras.utils import to_categorical


# Paths to your dataset folders
train_dir = 'rps'
test_dir = 'rps-test-set'

# The size to which you want to resize your images (this should be the same size as the input layer of your network)
img_size = (300, 300)

# Initialize lists to hold the images and labels
train_images = []
train_labels = []

test_images = []
test_labels = []

# Dictionary mapping label names to numeric values
label_to_index = {'rock': 0, 'paper': 1, 'scissors': 2}

# Function to load images from a directory
def load_images_and_labels(data_dir, images, labels):
    for label_name in os.listdir(data_dir):
        class_dir = os.path.join(data_dir, label_name)
        if os.path.isdir(class_dir):
            for image_name in os.listdir(class_dir):
                image_path = os.path.join(class_dir, image_name)
                image = load_img(image_path, target_size=img_size)
                image = img_to_array(image)
                images.append(image)
                labels.append(label_to_index[label_name])


# Load the training data
load_images_and_labels(train_dir, train_images, train_labels)

# Convert lists to numpy arrays
train_images = np.array(train_images)
train_labels = np.array(train_labels)

# Load the test data
load_images_and_labels(test_dir, test_images, test_labels)

# Convert lists to numpy arrays
test_images = np.array(test_images)
test_labels = np.array(test_labels)

# Preprocess the data by scaling the pixel values to be between 0 and 1
train_images = train_images / 255.0
test_images = test_images / 255.0

# Convert labels to one-hot encoded vectors
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# Split the training data into training and validation sets
train_images, val_images, train_labels, val_labels = train_test_split(
    train_images, train_labels, test_size=0.2, random_state=42
)
