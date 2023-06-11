from PIL import Image, ImageEnhance, ImageDraw
import numpy as np
import cv2
import math
from sklearn.cluster import KMeans

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pink = (155, 0, 255)


def load_image():
    # Image loading
    image = Image.open("C:/Users/sinna/OneDrive/Documents/EPFL/Master/DuploBuster/DuploBuster_Software/XY/pics/end.jpg")
    image = np.array(image)
    return image

def filter_image(image, center):
    # min and max radius
    min_radius = 100
    max_radius = 300
    
    # Convert the NumPy array to a PIL Image object
    image_pil = Image.fromarray(image)

    # Enhance the contrast
    enhancer = ImageEnhance.Contrast(image_pil)
    image_enhanced = enhancer.enhance(1.0)

    # Convert the enhanced image back to a NumPy array
    image_filtered = np.array(image_enhanced)

    # Get the dimensions of the image
    width, height = image_filtered.shape[1], image_filtered.shape[0]

    # Create a mask with True for pixels within the desired range, and False for pixels outside
    mask = np.ones((height, width), dtype=bool)

    for y in range(height):
        for x in range(width):
            dist = np.sqrt((x - center[0])**2 + (y - center[1])**2)
            if dist < min_radius or dist > max_radius:
                mask[y, x] = False

    # Apply the mask to the image, setting the pixels outside the range to black
    image_filtered[~mask] = (0, 0, 0)

    return image_filtered

def center_image(image):
    # Convert the NumPy array to a PIL Image object
    image_pil = Image.fromarray(image)

    # Get the dimensions of the image
    width, height = image_pil.size

    # Calculate the center point
    center = (width // 2, height // 2)

    # Find the darkest circular shape in the image
    min_radius = 30
    max_radius = 80
    min_score = 0.1
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    gray_blur = cv2.GaussianBlur(gray, (5, 5), cv2.BORDER_DEFAULT)
    circles = cv2.HoughCircles(
        gray_blur,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=100,
        param2=10,
        minRadius=min_radius,
        maxRadius=max_radius
    )
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
    draw = ImageDraw.Draw(image_pil)
    draw.ellipse((center[0] - 5, center[1] - 5, center[0] + 5, center[1] + 5), fill=(255, 0, 0))

    return center


def regions_image(image, center):
    # Define the colors to look for (RGB format)
    tolerance = 120

    # Find the pixels that match the defined colors within the tolerance range
    colors = [red, green, blue, pink]
    regions = {color: [] for color in colors}

    for x in range(image.shape[1]):
        for y in range(image.shape[0]):
            pixel = image[y, x]
            for color in colors:
                if all(abs(pixel[i] - color[i]) <= tolerance for i in range(3)):
                    regions[color].append((x, y))
                    break

    # Find the average polar coordinates of pixels in each color region
    polar_coords = {}
    for color, pixels in regions.items():
        if not pixels:
            continue
        pixels = np.array(pixels)
        x_coords = pixels[:, 0]
        y_coords = pixels[:, 1]

        # Perform clustering using K-means
        kmeans = KMeans(n_clusters=1, random_state=0).fit(pixels)
        cluster_center = kmeans.cluster_centers_[0]

        polar_r = np.sqrt((cluster_center[0] - center[0]) ** 2 + (cluster_center[1] - center[1]) ** 2)
        polar_theta = np.arctan2(cluster_center[1] - center[1], cluster_center[0] - center[0])
        polar_coords[color] = (np.mean(polar_r), np.mean(polar_theta))

    # Sort the polar coordinates based on the probability (number of pixels in each color region)
    sorted_polar_coords = sorted(polar_coords.items(), key=lambda x: len(regions[x[0]]), reverse=True)

    # Display the regions and center point in descending order
    for color, pixels in sorted_polar_coords:
        color_name = {
            red: "red",
            green: "green",
            blue: "blue",
            pink: "pink"
        }.get(color, str(color))
        print(f"Found {len(regions[color])} pixels of color {color_name}.")

    return dict(sorted_polar_coords)


def angles_polar(polar_coords):
    angles = {}
    for color, coords in polar_coords.items():
        if coords is None:
            angles[color] = None
        else:
            r, theta = coords
            # Calculate the angle based on polar coordinates
            angles[color] = math.degrees(theta)

    # Display the angles and color information
    for color, angle_value in angles.items():
        color_name = {
            red: "red",
            green: "green",
            blue: "blue",
            pink: "pink"
        }.get(color, str(color))
        if angle_value is None:
            print(f"No angle information for color {color_name}")
        else:
            print(f"Angle for color {color_name}: {angle_value} degrees")

    return angles

def angles_polar_relative(polar_coords):
    angle_relative = {}
    color_pairs = [
        (pink, red),
        (red, blue),
        (blue, green)
    ]

    for color_pair in color_pairs:
        color1, color2 = color_pair

        # Get the polar coordinates of the colors
        polar_coords1 = polar_coords.get(color1)
        polar_coords2 = polar_coords.get(color2)

        if polar_coords1 is None or polar_coords2 is None:
            # print("Missing angle information for color pair", color_pair)
            continue

        r1, theta1 = polar_coords1
        r2, theta2 = polar_coords2

        # Calculate the relative angle
        relative_angle = theta2 - theta1

        if color_pair not in angle_relative:
            angle_relative[color_pair] = []

        angle_relative[color_pair].append(math.degrees(relative_angle))

        # Display the relative angle with RGB color values
        color1_name = {
            red: "red",
            green: "green",
            blue: "blue",
            pink: "pink"
        }.get(color1, str(color1))
        color2_name = {
            red: "red",
            green: "green",
            blue: "blue",
            pink: "pink"
        }.get(color2, str(color2))
        print(f"Relative angle between {color1_name} and {color2_name}: {math.degrees(relative_angle)} degrees")

    return angle_relative
