import cv2
import matplotlib.pyplot as plt

def load_image():
    # Open the camera
    cap = cv2.VideoCapture(0)  # 0 is the camera index, you can change it to use another camera

    # Check if camera was successfully opened
    if not cap.isOpened():
        print("Error opening camera")
        exit()

    # Capture a frame
    ret, frame = cap.read()

    # Check if frame was successfully captured
    if not ret:
        print("Error capturing frame")
        exit()

    # Release the camera
    cap.release()

    # Convert BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Display the frame
    plt.imshow(frame)
    plt.show()

    return frame
