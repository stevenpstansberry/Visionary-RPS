import cv2



def startCapture(capture):

    # Check if the camera opened successfully
    if not capture.isOpened():
        print("Error: Could not open camera.")
        exit()

    # Continuously capture frames from the camera
    while True:
        ret, frame = capture.read()

        # If frame is read correctly, ret is True
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break

        # Display the resulting frame
        cv2.imshow('Webcam', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    capture.release()
    cv2.destroyAllWindows()