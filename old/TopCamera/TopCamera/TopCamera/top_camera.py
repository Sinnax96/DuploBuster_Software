from PIL import Image, ImageEnhance, ImageDraw
import numpy as np
import cv2
import math

# Load the image
image = Image.open("C:/Users/sinna/OneDrive/Documents/EPFL/Master/DuploBuster/DuploBuster_Software/TopCamera/pics.jpg")

# Enhance the contrast
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(2.0)

# Define the colors to look for (RGB format)
tolerance = 120  # Increase or decrease as needed
colors = [(255, 0, 0),  # Red
          (0, 255, 0),  # Green
          (0, 0, 255),  # Blue
          (255, 192, 203)] # pink  yellow -> (255, 255, 0)

# Find the pixels that match the defined colors within the tolerance range
regions = {}
for color in colors:
    pixels = []
    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))
            if abs(pixel[0] - color[0]) <= tolerance and \
               abs(pixel[1] - color[1]) <= tolerance and \
               abs(pixel[2] - color[2]) <= tolerance:
                pixels.append((x, y))
    regions[color] = pixels

# Set the center point to the middle of the image
center = (image.width // 2, image.height // 2)

# Find the brightest circular shape in the image
min_radius = 30
max_radius = 80
min_score = 0.1
gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
gray_blur = cv2.GaussianBlur(gray, (5,5), cv2.BORDER_DEFAULT)
circles = cv2.HoughCircles(gray_blur, cv2.HOUGH_GRADIENT, dp=1, minDist=50, 
                           param1=100, param2=10, minRadius=min_radius, maxRadius=max_radius)
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    for (x, y, r) in circles:
        mask = np.zeros(gray.shape, dtype=np.uint8)
        cv2.circle(mask, (x, y), r, 255, -1)
        mask_inv = cv2.bitwise_not(mask)
        brightness = np.mean(gray[mask_inv == 255])
        score = brightness / 255 * (r - min_radius) / (max_radius - min_radius)
        if score > min_score:
            center = (x, y)
            break

# Draw a red dot at the center point
draw = ImageDraw.Draw(image)
draw.ellipse((center[0]-5, center[1]-5, center[0]+5, center[1]+5), fill=(255,0,0))

# # Display the regions and center point
for color, pixels in regions.items():
    print(f"Found {len(pixels)} pixels of color {color}.")

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


# Plot lines from the center point to the average polar coordinates of each color region
draw = ImageDraw.Draw(image)
for color, polar_coord in polar_coords.items():
    polar_r, polar_theta = polar_coord
    x = center[0] + polar_r * np.cos(polar_theta)
    y = center[1] + polar_r * np.sin(polar_theta)
    draw.line((center[0], center[1], x, y), fill=color, width=5)

# Compute the angle of each line
angles = {}
for color, polar_coord in polar_coords.items():
    polar_r, polar_theta = polar_coord
    angle_deg = np.rad2deg(polar_theta)
    angles[color] = angle_deg
    print(f"The angle of the {color} line is {angle_deg:.2f} degrees.")

# Display the regions, center point, and lines
image.show()

# Define the dimensions of the room in meters
X = 8
Y = 8

# Angle between corner
# Compute the angle between each line
angles_lines = {}
colors = list(polar_coords.keys())
for i in range(len(colors)):
    for j in range(i+1, len(colors)):
        color1, color2 = colors[i], colors[j]
        polar_coord1, polar_coord2 = polar_coords[color1], polar_coords[color2]
        polar_theta1, polar_theta2 = polar_coord1[1], polar_coord2[1]
        angle_deg = abs(np.rad2deg(polar_theta2 - polar_theta1))
        angles_lines[(color1, color2)] = angle_deg
        print(f"The angle between the {color1} and {color2} lines is {angle_deg:.2f} degrees.")

# Find alpha and beta
beta = 90 - angles[(0, 0, 255)]
alpha = 180 - beta - angles_lines[(0, 0, 255), (255, 192, 203)]

# Find alphap and betap
betap = 90 - angles[(0, 255, 0)]
alphap = 90 - beta

# x,y position
y = X * math.sin(alpha) * math.sin(beta) / math.sin(alpha+beta)
x = Y * math.sin(alphap) * math.sin(betap) / math.sin(alphap+betap)

print(y)
print(x)


