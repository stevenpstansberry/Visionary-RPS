# webcam_feed.py handles the activation of the webcam


import cv2

def startCapture():
    """
    Initializes the webcam video capture object.
    
    Returns:
        cap: The video capture object.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        cap = None  # or raise an exception
    return cap

def getFrame(cap):
    """
    Retrieves the current frame from the video capture object.

    Args:
        cap: The video capture object.

    Returns:
        frame: The current video frame.
    """
    ret, frame = cap.read()
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        return None
    return frame

def stopCapture(cap):
    """
    Releases the video capture object.

    Args:
        cap: The video capture object.
    """
    cap.release()
