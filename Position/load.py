from PIL import Image, ImageEnhance, ImageDraw
import numpy as np
import cv2
import math
from sklearn.cluster import KMeans

red = (255, 0, 50)
green = (0, 255, 100)
blue = (0, 150, 255)
pink = (200, 0, 255)


def load_image():
    # Image loading
    image = Image.open("C:/Users/sinna/OneDrive/Documents/EPFL/Master/DuploBuster/DuploBuster_Software/Position/final_pics/44180.jpg")
    image = np.array(image)
    return image

def filter_image(image, factor):
    # Convert the NumPy array to PIL Image
    image = Image.fromarray(np.uint8(image))

    # Calculate the new dimensions
    width, height = image.size
    new_width = width // factor
    new_height = height // factor

    # Resize the image
    new_image = image.resize((new_width, new_height), Image.ANTIALIAS)

    # Enhance the contrast
    enhancer = ImageEnhance.Contrast(new_image)
    enhanced_image = enhancer.enhance(2)

    # Convert the resized image back to NumPy array
    filtered_image = np.array(new_image)

    return filtered_image

def center_image(image):
    # Convert the NumPy array to a PIL Image object
    image_pil = Image.fromarray(image)

    # Get the dimensions of the image
    width, height = image_pil.size

    # Calculate the center point
    center = (width // 2, height // 2)

    # Find the darkest circular shape in the image
    min_radius = 30
    max_radius = 50
    min_score = 0.1
    max_distance = min(width, height) // 8
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
        min_distance = np.inf
        for (x, y, r) in circles:
            distance = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
            if distance < min_distance and distance < max_distance:
                mask = np.zeros(gray.shape, dtype=np.uint8)
                cv2.circle(mask, (x, y), r, 255, -1)
                mask_inv = cv2.bitwise_not(mask)
                brightness = np.mean(gray[mask_inv == 0])
                score = (255 - brightness) / 255 * (r - min_radius) / (max_radius - min_radius)
                if score > min_score and brightness < min_brightness:
                    center = (x, y)
                    min_brightness = brightness
                    min_distance = distance

    # Draw a red dot at the center point
    draw = ImageDraw.Draw(image_pil)
    draw.ellipse((center[0] - 5, center[1] - 5, center[0] + 5, center[1] + 5), fill=(255, 0, 0))

    return center


def regions_image(image, center):
    # Define the colors to look for (RGB format)
    tolerance = 110

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

