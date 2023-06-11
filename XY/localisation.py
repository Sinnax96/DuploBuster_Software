import math

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pink = (155, 0, 255)
def localisation(angle, angle_relative, sorted_polar_coords):
    # Extract the sorted polar coordinates for each color
    green_coords = sorted_polar_coords[0][1]
    blue_coords = sorted_polar_coords[1][1]
    red_coords = sorted_polar_coords[2][1]
    pink_coords = sorted_polar_coords[3][1]

    # Extract the angles for each color
    green_angle = angle[green]
    blue_angle = angle[blue]
    red_angle = angle[red]
    pink_angle = angle[pink]

    # Calculate the relative angles
    relative_angles = {
        (green, blue): blue_angle - green_angle,
        (blue, red): red_angle - blue_angle,
        (red, pink): pink_angle - red_angle,
        (pink, green): green_angle - pink_angle
    }

    # Calculate the relative position of the robot
    relative_position = {
        (green, blue): (0, 0),
        (blue, red): (0, 1),
        (red, pink): (1, 1),
        (pink, green): (1, 0)
    }

    # Calculate the absolute position of the robot
    x = green_coords[0] * math.cos(math.radians(green_angle))
    y = green_coords[0] * math.sin(math.radians(green_angle))

    # Calculate the relative angle of the robot
    relative_angle = sum(relative_angles.values())

    return x, y, relative_angle
