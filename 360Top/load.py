from PIL import Image, ImageEnhance, ImageDraw
import numpy as np
import cv2
import math

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pink = (155, 0, 255)

def load_image():
    # Image loading
    image = Image.open("C:/Users/sinna/OneDrive/Documents/EPFL/Master/DuploBuster/DuploBuster_Software/360Top/pics/start.jpg")
    image = np.array(image)
    return image

def filter_image(image):
    # Convert the NumPy array to a PIL Image object
    image_pil = Image.fromarray(image)

    # Enhance the contrast
    enhancer = ImageEnhance.Contrast(image_pil)
    image_enhanced = enhancer.enhance(1.0)

    # Convert the enhanced image back to a NumPy array
    image_filtered = np.array(image_enhanced)

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
        polar_r = np.sqrt((x_coords - center[0]) ** 2 + (y_coords - center[1]) ** 2)
        polar_theta = np.arctan2(y_coords - center[1], x_coords - center[0])
        polar_coords[color] = (np.mean(polar_r), np.mean(polar_theta))

    # # Display the regions and center point
    # for color, pixels in regions.items():
    #     color_name = {
    #         red: "red",
    #         green: "green",
    #         blue: "blue",
    #         pink: "pink"
    #     }.get(color, str(color))
    #     print(f"Found {len(pixels)} pixels of color {color_name}.")


    # Sort the polar coordinates based on the number of pixels in each color region
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

    return sorted_polar_coords

def angles_polar(polar_coords):
    angle = {}
    for color, coords in polar_coords.items():
        r, theta = coords
        # Calculate the angle based on polar coordinates
        angle[color] = math.degrees(theta)

    # Display the angles and color information
    for color, angle_value in angle.items():
        color_name = {
            red: "red",
            green: "green",
            blue: "blue",
            pink: "pink"
        }.get(color, str(color))
        print(f"Angle for color {color_name} : {angle_value} degrees")

    return angle

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
