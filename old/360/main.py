from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import numpy as np
import math
import cv2

from plot import plot

def filter_image(image):
    # Convert the NumPy array to a PIL Image object
    image_pil = Image.fromarray(image)

    # Enhance the contrast
    enhancer = ImageEnhance.Contrast(image_pil)
    image_enhanced = enhancer.enhance(1.0)

    # Convert the enhanced image back to a NumPy array
    image_filtered = np.array(image_enhanced)

    return image_filtered


def load_image():
    # Image loading
    image = Image.open("C:/Users/sinna/OneDrive/Documents/EPFL/Master/DuploBuster/DuploBuster_Software/360/start.jpg")
    image = np.array(image)
    return image

def center_image(image):
    # Convert the NumPy array to a PIL Image object
    image = Image.fromarray(image)

    # Get the dimensions of the image
    width, height = image.size

    # Calculate the center point
    center = (width // 2, height // 2)

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


    # Draw a red dot at the center point
    draw = ImageDraw.Draw(image)
    draw.ellipse((center[0] - 5, center[1] - 5, center[0] + 5, center[1] + 5), fill=(255, 0, 0))


    return center

def regions_image(image, center):
    # Define the colors to look for (RGB format)
    tolerance = 120  # Variable
    # Find colors region
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    pink = (255, 0, 255)

    # Find the pixels that match the defined colors within the tolerance range
    regions = {}
    for color in [red, green, blue, pink]:
        pixels = []
        for x in range(image.shape[1]):
            for y in range(image.shape[0]):
                pixel = image[y, x]
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
        if color == red:
            color_name = "red"
        elif color == green:
            color_name = "green"
        elif color == blue:
            color_name = "blue"
        elif color == pink:
            color_name = "pink"
        else:
            color_name = str(color)
        print(f"Found {len(pixels)} pixels of color {color_name}.")

    return regions, polar_coords



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
    color_pairs = [((255, 0, 255), (255, 0, 0)),
                   ((255, 0, 0), (0, 0, 255)),
                   ((0, 0, 255), (0, 255, 0))]

    # Calculate the angles between color pairs
    for color_pair in color_pairs:
        color1, color2 = color_pair

        # Get the polar coordinates of the colors
        polar_coords1 = polar_coords.get(color1)
        polar_coords2 = polar_coords.get(color2)

        if polar_coords1 is None or polar_coords2 is None:
            print("Missing angle information for color pair", color_pair)
            continue

        r1, theta1 = polar_coords1
        r2, theta2 = polar_coords2

        # Calculate the relative angle
        relative_angle = theta2 - theta1

        if color_pair not in angle_relative:
            angle_relative[color_pair] = []

        angle_relative[color_pair].append(math.degrees(relative_angle))

        # Print the relative angle
        print(f"Relative angle between {color1} and {color2}: {math.degrees(relative_angle)} degrees")

    return angle_relative


def triangulation(angle, angle_relative, dimensions):
    # Perform triangulation to estimate the relative angle
    print(angle)
    # Perform triangulation to estimate the position
    positions = []
    for color_pair, angles in angle_relative.items():
        if len(angles) >= 2:
            alpha = angles[0]
            beta = angles[1]

            x = dimensions[0] * math.sin(math.radians(alpha)) * math.sin(math.radians(beta)) / \
                math.sin(math.radians(alpha + beta))
            y = dimensions[1] * math.sin(math.radians(alpha)) * math.sin(math.radians(180 - beta)) / \
                math.sin(math.radians(alpha + beta))

            positions.append((x, y))

    if positions:
        avg_x = sum(p[0] for p in positions) / len(positions)
        avg_y = sum(p[1] for p in positions) / len(positions)
        return avg_x, avg_y
    else:
        return None, None

def main():
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

    # Set dimensions for triangulation
    dimensions = (8, 8)

    # Find position
    position_x, position_y = triangulation(angle, angle_relative, dimensions)
    if position_x is not None and position_y is not None:
        print("Estimated position:", position_x, position_y)
    else:
        print("Unable to estimate position.")

    # Plot
    plot(image, center, polar_coords)

if __name__ == "__main__":
    main()
