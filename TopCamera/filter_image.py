from PIL import Image, ImageEnhance, ImageDraw
import numpy as np
import cv2
import math

def filter_image(image):

    # Enhance the contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)

    return image