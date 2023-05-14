from PIL import Image
import numpy as np

from filter_image import filter_image
from load_image import load_image
from regions_image import regions_image
from center_image import center_image
from polar_coords import polar_coords
from plot import plot
from angles_polar import angles_polar

# Load the image
image = Image.open("C:/Users/sinna/OneDrive/Documents/EPFL/Master/DuploBuster/DuploBuster_Software/TopCamera/pics.jpg")
# image = load_image()

# Filter image
image = filter_image(image)

# Find center
center = center_image(image)

regions = regions_image(image, center)

# Find avg polar coords
avg_polar = polar_coords(regions, center)

# plot(image,center,avg_polar)

# # Compute angle and relative angles
# angle = angles_polar(avg_polar)
# angle_relative = angles_polar_relative(avg_polar)

# # Find position
# position = triangulation(angle, angle_relative)

image.show()