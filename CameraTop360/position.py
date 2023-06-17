from load import load_image, filter_image, center_image, regions_image
from plot import plot
from triangulation import triangulation
from capture import capture

def position(cap):
    # Load the image
    image = capture(cap)
    # image = load_image()

    # Filter image
    image = filter_image(image)

    # Find center
    center = center_image(image)

    # Find LEDs polar coords
    sorted_polar_coords = regions_image(image, center)

    # Find position
    position_x, position_y, relative_angle = triangulation(sorted_polar_coords)

    # Plot
    # plot(image, center, sorted_polar_coords)
    # print(f"Position X: {position_x} Position Y: {position_y} Angle: {relative_angle}")

    return position_x, position_y, relative_angle


