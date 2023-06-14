import cv2

from position import position

def main():
    # Initialize the video capture object
    cap = cv2.VideoCapture(0)

    position_x, position_y, relative_angle = position(cap)

    # Release the video capture object
    cap.release()

