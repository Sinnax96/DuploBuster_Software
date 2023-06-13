import cv2

def capture():
    # Settings
    exposure_time = 0.001
    # Initialize the video capture object
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # Adjust camera settings
    if exposure_time is not None:
        cap.set(cv2.CAP_PROP_EXPOSURE, exposure_time)

    # Capture the frame
    ret, frame = cap.read()

    # Check if the frame is captured correctly
    if not ret:
        raise RuntimeError("Failed to capture image")

    # Release the video capture object
    cap.release()

    # Save the captured image
    cv2.imwrite('C:/Users/sinna/OneDrive/Documents/EPFL/Master/DuploBuster/DuploBuster_Software/XY/final_pics/110.jpg', frame)

    cv2.destroyAllWindows()

    return frame
