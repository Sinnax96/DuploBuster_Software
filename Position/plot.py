from PIL import Image, ImageEnhance, ImageDraw
import numpy as np
import math
import cv2

red = (255, 0, 50)
green = (0, 255, 100)
blue = (0, 150, 255)
pink = (200, 0, 255)

def plot(image, center, sorted_polar_coords):
    # Convert the NumPy array to a PIL Image object
    image_pil = Image.fromarray(image)

    # Create an ImageDraw object
    draw = ImageDraw.Draw(image_pil)

    # Draw a red dot at the center point
    draw.ellipse((center[0] - 5, center[1] - 5, center[0] + 5, center[1] + 5), fill=(255, 0, 0))

    # Get the sorted colors in the order of number of pixels
    sorted_colors = [color for color in sorted_polar_coords]

    # Plot a line from the center point to the average polar coordinates of each color region
    for color in sorted_colors:
        avg_polar_coords = sorted_polar_coords[color]
        if avg_polar_coords is not None:
            avg_polar_r, avg_polar_theta = avg_polar_coords
            color_name = {
                red: "red",
                green: "green",
                blue: "blue",
                pink: "pink"
            }.get(color, str(color))
            if not math.isnan(avg_polar_r) and not math.isnan(avg_polar_theta):
                x = center[0] + avg_polar_r * math.cos(avg_polar_theta)
                y = center[1] + avg_polar_r * math.sin(avg_polar_theta)

                draw.line((center[0], center[1], x, y), fill=color, width=5)
                print(f"{color_name}: {math.degrees(avg_polar_theta)} degrees")
            else:
                print(f"{color_name}: None")

    # Display the image
    image_pil.show()
