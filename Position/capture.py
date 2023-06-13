import cv2

def capture():
    # Initialize the video capture object
    print("f")
    cap = cv2.VideoCapture(0)
    print("c")
    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    print("b")
    # Capture the frame
    ret, frame = cap.read()
    print("a")

    # Check if the frame is captured correctly
    if not ret:
        raise RuntimeError("Failed to capture image")
    print("d")
    # Release the video capture object
    cap.release()
    print("e")
    # Save the captured image
    cv2.imwrite('C:/Users/sinna/OneDrive/Documents/EPFL/Master/DuploBuster/DuploBuster_Software/Position/final_pics/47180.jpg', frame)

    return frame