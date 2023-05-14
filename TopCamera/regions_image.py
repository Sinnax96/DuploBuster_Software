import numpy as np

def regions_image(image, center):
    # Define the colors to look for (RGB format)
    tolerance = 120  # Increase or decrease as needed
    # Find colors region
    colors = [(0, 0, 0)]  # Black circle

    # Find the pixels that match the defined colors within the tolerance range
    regions = []
    for color in colors:
        pixels = []
        for x in range(image.width):
            for y in range(image.height):
                pixel = image.getpixel((x, y))
                if abs(pixel[0] - color[0]) <= tolerance and \
                abs(pixel[1] - color[1]) <= tolerance and \
                abs(pixel[2] - color[2]) <= tolerance:
                    pixels.append((x, y))
        regions.append((color, pixels))

    # Find the average polar coordinates of pixels in each color region
    polar_coords = {}
    for color, pixels in regions:
        try:
            polar_r, polar_theta = calculate_polar_coords(pixels, center)
            polar_coords[color] = (np.mean(polar_r), np.mean(polar_theta))
        except ValueError:
            # No pixels found in this color region
            continue

    # # Display the regions and center point
    for color, pixels in regions:
        print(f"Found {len(pixels)} pixels of color {color}.")

    return regions, polar_coords


def calculate_polar_coords(pixels, center):
    x_coords, y_coords = zip(*pixels)
    x_coords = np.array(x_coords)
    y_coords = np.array(y_coords)
    polar_r = np.sqrt((x_coords - center[0])**2 + (y_coords - center[1])**2)
    polar_theta = np.arctan2(y_coords - center[1], x_coords - center[0])
    return polar_r, polar_theta
