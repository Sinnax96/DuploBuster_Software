from PIL import ImageDraw
import numpy as np

def plot(image, center, polar_coords):
    # Draw a red dot at the center point
    draw = ImageDraw.Draw(image)
    draw.ellipse((center[0]-5, center[1]-5, center[0]+5, center[1]+5), fill=(255,0,0))

    # Plot lines from the center point to the average polar coordinates of each color region
    draw = ImageDraw.Draw(image)
    for color, polar_coord in polar_coords.items():
        polar_r, polar_theta = polar_coord
        x = center[0] + polar_r * np.cos(polar_theta)
        y = center[1] + polar_r * np.sin(polar_theta)
        draw.line((center[0], center[1], x, y), fill=color, width=5)