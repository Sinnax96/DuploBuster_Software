from PIL import ImageDraw
import numpy as np

def polar_coords(regions, center):
    # Find the average polar coordinates of pixels in each color region
    polar_coords = {}
    for color, pixels in regions.items():
        try:
            x_coords, y_coords = zip(*pixels)
        except ValueError:
            # No pixels found in this color region
            continue
        x_coords = np.array(x_coords)
        y_coords = np.array(y_coords)
        polar_r = np.sqrt((x_coords - center[0])**2 + (y_coords - center[1])**2)
        polar_theta = np.arctan2(y_coords - center[1], x_coords - center[0])
        polar_coords[color] = (np.mean(polar_r), np.mean(polar_theta))

    return polar_coords