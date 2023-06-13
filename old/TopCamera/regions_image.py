import math

def regions_image(image, center):
    # Define the colors to look for (RGB format)
    tolerance = 120  # Increase or decrease as needed
    # Find colors region
    colors = [(255, 0, 0),  # Red
              (0, 255, 0),  # Green
              (0, 0, 255),  # Blue
              (255, 0, 255)] # Pink

    # Find the pixels that match the defined colors within the tolerance range
    regions = {}
    for color in colors:
        pixels = []
        for x in range(image.width):
            for y in range(image.height):
                pixel = image.getpixel((x, y))
                if (abs(pixel[0] - color[0]) <= tolerance and
                    abs(pixel[1] - color[1]) <= tolerance and
                    abs(pixel[2] - color[2]) <= tolerance):
                    pixels.append((x, y))
        regions[color] = pixels

    # Find the average polar coordinates of pixels in each color region
    polar_coords = {}
    for color, pixels in regions.items():
        if not pixels:
            continue
        x_coords, y_coords = zip(*pixels)
        x_coords = list(x_coords)
        y_coords = list(y_coords)
        polar_r = [math.sqrt((x - center[0])**2 + (y - center[1])**2) for x, y in zip(x_coords, y_coords)]
        polar_theta = [math.atan2(y - center[1], x - center[0]) for x, y in zip(x_coords, y_coords)]
        polar_coords[color] = (sum(polar_r) / len(polar_r), sum(polar_theta) / len(polar_theta))

    # Display the regions and center point
    for color, pixels in regions.items():
        print(f"Found {len(pixels)} pixels of color {color}.")

    return regions, polar_coords