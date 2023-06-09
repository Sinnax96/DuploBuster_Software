from PIL import Image
import numpy as np
import math

from plot import plot

def filter_image(image):
    # Apply any necessary image filtering operations here
    filtered_image = image
    return filtered_image

def load_image():
    # Implement your image loading logic here
    image = Image.open("C:/Users/sinna/OneDrive/Documents/EPFL/Master/DuploBuster/DuploBuster_Software/TopCamera/pic.jpg")
    return image

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
        pixels = np.array(pixels)
        x_coords = pixels[:, 0]
        y_coords = pixels[:, 1]
        polar_r = np.sqrt((x_coords - center[0])**2 + (y_coords - center[1])**2)
        polar_theta = np.arctan2(y_coords - center[1], x_coords - center[0])
        polar_coords[color] = (np.mean(polar_r), np.mean(polar_theta))

    # Display the regions and center point
    for color, pixels in regions.items():
        print(f"Found {len(pixels)} pixels of color {color}.")

    return regions, polar_coords

def center_image(image):
    # Implement your center-finding logic here
    center = (image.width // 2, image.height // 2)
    return center

def angles_polar(polar_coords):
    # Implement your polar angle calculation logic here
    angle = {}
    for color, coords in polar_coords.items():
        r, theta = coords
        # Calculate the angle based on polar coordinates
        angle[color] = math.degrees(theta)
    return angle

def angles_polar_relative(polar_coords):
    # Implement your relative angle calculation logic here
    angle_relative = {}
    # Calculate the relative angles between color pairs
    color_pairs = [((255, 0, 0), (0, 255, 0)),
                   ((0, 0, 255), (0, 255, 0)),
                   ((0, 0, 255), (255, 0, 255))]
    for color1, color2 in color_pairs:
        if color1 in polar_coords and color2 in polar_coords:
            theta1 = polar_coords[color1][1]
            theta2 = polar_coords[color2][1]
            # Calculate the relative angle
            relative_angle = theta2 - theta1
            angle_relative[(color1, color2)] = math.degrees(relative_angle)
    return angle_relative

def triangulation(angle, angle_relative):
    # Define the dimensions of the room in meters
    X = 8
    Y = 8

    positions = []

    # Define the color pairs
    color_pairs = [((255, 0, 0), (0, 255, 0)),
                   ((0, 0, 255), (0, 255, 0)),
                   ((0, 0, 255), (255, 0, 255))]

    for color_pair in color_pairs:
        color1, color2 = color_pair

        # Find alpha and beta
        angle1 = angle.get(color1)
        angle2 = angle.get(color2)
        angle_relative_pair = angle_relative.get(color_pair)

        if angle1 is None or angle2 is None or angle_relative_pair is None:
            print("Missing angle information for color pair", color_pair)
            continue

        beta = 90 - angle1
        alpha = 180 - beta - angle_relative_pair

        # Find alphap and betap
        angle3 = angle.get((0, 255, 0))
        if angle3 is None:
            print("Missing angle information for color (0, 255, 0)")
            continue

        betap = 90 - angle3
        alphap = 90 - beta

        # Calculate x and y positions
        y = X * math.sin(math.radians(alpha)) * math.sin(math.radians(beta)) / math.sin(math.radians(alpha + beta))
        x = Y * math.sin(math.radians(alphap)) * math.sin(math.radians(betap)) / math.sin(math.radians(alphap + betap))

        positions.append((x, y))

    if len(positions) == 0:
        print("No valid positions calculated")
        return

    # Calculate the average position
    avg_x = sum(p[0] for p in positions) / len(positions)
    avg_y = sum(p[1] for p in positions) / len(positions)

    print("Estimated position:")
    print("x:", avg_x)
    print("y:", avg_y)

# Load the image
image = load_image()

# Filter image
image = filter_image(image)

# Find center
center = center_image(image)

# Find avg polar coords
regions, polar_coords = regions_image(image, center)

# Compute angle and relative angles
angle = angles_polar(polar_coords)
angle_relative = angles_polar_relative(polar_coords)

# Find position
triangulation(angle, angle_relative)

# Plot
plot(image, center, polar_coords)
