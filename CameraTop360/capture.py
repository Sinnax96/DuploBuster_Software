import cv2

def capture(cap):

    exposure_time = 0.0001
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

    return frame