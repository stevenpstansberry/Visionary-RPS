import webcam_feed
import tensorflow_datasets
import cv2

def main():
    capture = webcam_feed.startCapture()


    if capture is not None:
        while True:
            frame = webcam_feed.getFrame(capture)
            if frame is None:
                break
            
            # Display the frame
            cv2.imshow('Webcam Feed', frame)

            # Break the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        webcam_feed.stopCapture(capture)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()