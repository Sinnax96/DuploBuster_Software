import cv2

def capture(cap):
    # # Initialize the video capture object
    # cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    # Capture the frame
    ret, frame = cap.read()

    # Check if the frame is captured correctly
    if not ret:
        raise RuntimeError("Failed to capture image")

    # # Release the video capture object
    # cap.release()

    return frame