import math

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pink = (155, 0, 255)

def triangulation(sorted_polar_coords):
    # Define the dimensions of the room in meters
    distance = 8

    angles = {}

    for color, (polar_r, polar_theta) in sorted_polar_coords.items():
        angles[color] = math.degrees(polar_theta)

    angle_pink = angles.get(pink)
    angle_green = angles.get(green)
    angle_red = angles.get(red)
    angle_blue = angles.get(blue)

    # Change of reference
    if angle_pink is not None:
        angle_pink = -angle_pink
        print("Angle (Pink):", angle_pink)
        # angle_relative_pink = angle_pink - 45
        # print("Relative angle (Pink):", angle_relative_pink)

    if angle_green is not None:
        angle_green = -angle_green
        print("Angle (Green):", angle_green)
        # angle_relative_green = angle_green + 225
        # print("Relative angle (Green):", angle_relative_green)

    if angle_red is not None:
        angle_red = -angle_red
        print("Angle (Red):", angle_red)
        # angle_relative_red = angle_red + 45
        # print("Relative angle (Red):", angle_relative_red)

    if angle_blue is not None:
        angle_blue = -angle_blue
        print("Angle (Blue):", angle_blue)
        # angle_relative_blue = angle_blue + 135
        # print("Relative angle (Blue):", angle_relative_blue)

    valid_data_points = 0
    position_x_sum = 0
    position_y_sum = 0

    # angle_red + angle_pink
    if angle_red is not None and angle_pink is not None:
        h_rp = distance * math.sin(math.radians(angle_red)) / math.sin(math.radians(angle_pink - angle_red))

        position_x_rp = h_rp * math.cos(math.radians(180 - angle_pink))
        position_y_rp = distance - h_rp * math.sin(math.radians(180 - angle_pink))
        print("Position from Red-Pink:", position_x_rp, position_y_rp)
        print("")
        if 0 <= position_x_rp <= distance and 0 <= position_y_rp <= distance:
            valid_data_points += 1
            position_x_sum += position_x_rp
            position_y_sum += position_y_rp

    # angle_pink + angle_green
    if angle_pink is not None and angle_green is not None:
        h_pg = distance * math.sin(math.radians(angle_pink - 90)) / math.sin(math.radians(angle_green - angle_pink))
        position_x_pg = h_pg * math.cos(math.radians(180 + angle_green))
        position_y_pg = h_pg * math.sin(math.radians(180 + angle_green))
        print("Position from Pink-Green:", position_x_pg, position_y_pg)
        print("")
        if 0 <= position_x_rp <= distance and 0 <= position_y_rp <= distance:
            valid_data_points += 1
            position_x_sum += position_x_pg
            position_y_sum += position_y_pg

    # angle_green + angle_blue
    if angle_green is not None and angle_blue is not None:
        h_gb = distance * math.sin(math.radians(180 + angle_green)) / math.sin(math.radians(angle_blue - angle_green))
        position_x_gb = distance - h_gb * math.cos(math.radians(angle_blue))
        position_y_gb = -h_gb * math.sin(math.radians(angle_blue))
        print("Position from Green-Blue:", position_x_gb, position_y_gb)
        print("")

        if 0 <= position_x_rp <= distance and 0 <= position_y_rp <= distance:
            valid_data_points += 1
            position_x_sum += position_x_gb
            position_y_sum += position_y_gb

    if valid_data_points > 0:
        position_x = position_x_sum / valid_data_points
        position_y = position_y_sum / valid_data_points
    else:
        position_x = None
        position_y = None

    x, y, relative_angle = position_x, position_y, 0

    print(f"Position X: {x} Position Y: {y} Angle: {relative_angle}")

    return x, y, relative_angle
