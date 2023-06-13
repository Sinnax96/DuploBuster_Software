import math

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pink = (155, 0, 255)

def triangulation(sorted_polar_coords):
    # Define the dimensions of the room in meters
    X = 8
    Y = 8

    # First compute relative angle of robot
    angle = {color: polar_coords[1] for color, polar_coords in sorted_polar_coords}

    relative_angle_pink = angle[pink] + 135
    relative_angle_green = angle[green] - 135
    relative_angle_red = angle[red] + 45
    relative_angle_blue = angle[blue] - 45

    # Adjust the range to -180 to 180
    relative_angle_pink = (relative_angle_pink + 180) % 360 - 180
    relative_angle_green = (relative_angle_green + 180) % 360 - 180
    relative_angle_red = (relative_angle_red + 180) % 360 - 180
    relative_angle_blue = (relative_angle_blue + 180) % 360 - 180

    print("Relative angle (Pink):", relative_angle_pink)
    print("Relative angle (Green):", relative_angle_green)
    print("Relative angle (Red):", relative_angle_red)
    print("Relative angle (Blue):", relative_angle_blue)

    # Look for outliers and remove them from the list, then average relative angles

    # Triangulation with remaining line colors
    # Case 4, 3, 2 line case

    x, y, relative_angle = 0, 0, 0

    return x, y, relative_angle