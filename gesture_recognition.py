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

# Print the total number of images and labels
print(f"Total training images: {len(train_images)}")
print(f"Total training labels: {len(train_labels)}")

# Assert the number of images and labels are the same
assert len(train_images) == len(train_labels), "The number of images and labels must be the same."

# Print the shape of the first few images and their corresponding labels
for i in range(2520):  # Just as an example, print out the first 5 images and labels
    print(f"Image {i} shape: {train_images[i].shape} - Label: {train_labels[i]}")




    