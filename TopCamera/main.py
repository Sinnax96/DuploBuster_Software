from PIL import Image
import numpy as np

from filter_image import filter_image
from load_image import load_image
from regions_image import regions_image
from center_image import center_image
from plot import plot
from angles_polar import angles_polar
from angles_polar_relative import angles_polar_relative
from triangulation import triangulation

# Load the image
image = Image.open("C:/Users/sinna/OneDrive/Documents/EPFL/Master/DuploBuster/DuploBuster_Software/TopCamera/pic.jpg")
# image = load_image()

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
# position = triangulation(angle, angle_relative)

# plot
plot(image,center,polar_coords)