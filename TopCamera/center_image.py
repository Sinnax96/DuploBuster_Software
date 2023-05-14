import cv2
import numpy as np
from PIL import ImageDraw

def center_image(image):
    # Set the center point to the middle of the image
    center = (image.width // 2, image.height // 2)

    # Find the darkest circular shape in the image
    min_radius = 30
    max_radius = 80
    min_score = 0.1
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    gray_blur = cv2.GaussianBlur(gray, (5,5), cv2.BORDER_DEFAULT)
    circles = cv2.HoughCircles(gray_blur, cv2.HOUGH_GRADIENT, dp=1, minDist=50, 
                            param1=100, param2=10, minRadius=min_radius, maxRadius=max_radius)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        min_brightness = np.inf
        for (x, y, r) in circles:
            mask = np.zeros(gray.shape, dtype=np.uint8)
            cv2.circle(mask, (x, y), r, 255, -1)
            mask_inv = cv2.bitwise_not(mask)
            brightness = np.mean(gray[mask_inv == 0])
            score = (255 - brightness) / 255 * (r - min_radius) / (max_radius - min_radius)
            if score > min_score and brightness < min_brightness:
                center = (x, y)
                min_brightness = brightness

    # # Draw a red dot at the center point
    # draw = ImageDraw.Draw(image)
    # draw.ellipse((center[0]-5, center[1]-5, center[0]+5, center[1]+5), fill=(255,0,0))

    return center
