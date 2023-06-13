from load import load_image, filter_image, center_image, regions_image, angles_polar, angles_polar_relative
from plot import plot
from triangulation import triangulation
from capture import capture
import cv2

from localisation import localisation

# Load the image
image = load_image()
# image = capture()

# Filter image
image = filter_image(image)

# Find center
center = center_image(image)

# Find LEDs polar coords
sorted_polar_coords = regions_image(image, center)

# Convert sorted_polar_coords to dictionary
polar_coords = dict(sorted_polar_coords)

# Plot
plot(image, center, polar_coords)

# Compute angle and relative angles
angle = angles_polar(polar_coords)
angle_relative = angles_polar_relative(polar_coords)

# Find position
position_x, position_y = triangulation(angle, angle_relative, sorted_polar_coords)
if position_x is not None and position_y is not None:
    print("Estimated position:", position_x, position_y)
else:
    print("Unable to estimate position.")


# x, y, relative_angle = localisation(angle, angle_relative, sorted_polar_coords)
# print("Estimated position:", x, y)


