from webcam_feed import startCapture
import tensorflow_datasets as tfds
import cv2

# Create capture object
cap = cv2.VideoCapture(0)

startCapture(cap)

