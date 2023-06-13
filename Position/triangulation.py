import math

from angle import filter_outliers

red = (255, 0, 50)
green = (0, 255, 100)
blue = (0, 150, 255)
pink = (200, 0, 255)

def triangulation(sorted_polar_coords):
    # Define the dimensions of the room in meters
    distance = 8

    # Get angles
    angles = {}
    for color, (polar_r, polar_theta) in sorted_polar_coords.items():
        angles[color] = math.degrees(polar_theta)
    
    angle_pink = angles.get(pink)
    angle_green = angles.get(green)
    angle_red = angles.get(red)
    angle_blue = angles.get(blue)

    # Get the first color and its polar angle
    first_color = next(iter(sorted_polar_coords))
    print("")
    print("first_color", first_color)

    # Get angles for all colors
    angles = {}
    for color, (polar_r, polar_theta) in sorted_polar_coords.items():
        angles[color] = math.degrees(polar_theta)

    # Compute relative angles
    relative_angle = 0

    if pink == first_color:
        relative_angle = angles[pink] + 135
    if red == first_color:
        relative_angle = angles[red] + 45
    if green == first_color:
        relative_angle = angles[green] - 135
    if blue == first_color:
        relative_angle = angles[blue] - 45

    if angle_pink is not None:
        angle_pink -= relative_angle
    if angle_green is not None:
        angle_green -= relative_angle
    if angle_red is not None:
        angle_red -= relative_angle
    if angle_blue is not None:
        angle_blue -= relative_angle

    valid_data_points = 0

    # angle_pink + angle_red
    position_x_pr = -1
    position_y_pr = -1
    if angle_red is not None and angle_pink is not None:
        # Law of sin
        h_pr = distance * math.sin(math.radians(180 + angle_pink)) / math.sin(math.radians(angle_red - angle_pink))

        position_x_pr = distance - h_pr * math.cos(math.radians(angle_red))
        position_y_pr = - h_pr * math.sin(math.radians(angle_red))
        print("Position from Pink-Red:", position_x_pr, position_y_pr)
        print("")
        # Remove line as it is noise and lead to position outside room
        if 0 <= position_x_pr <= distance and 0 <= position_y_pr <= distance:
            valid_data_points += 1

    ## angle_green + angle_pink
    position_x_gp = -1
    position_y_gp = -1
    if angle_pink is not None and angle_green is not None:
        h_gp = distance * math.sin(math.radians(angle_green -90)) / math.sin(math.radians(angle_pink - angle_green))

        position_x_gp = h_gp * math.cos(math.radians(180 + angle_pink))
        position_y_gp = h_gp * math.sin(math.radians(180 + angle_pink))
        print("Position from Green-Pink:", position_x_gp, position_y_gp)
        print("")
        if 0 <= position_x_gp <= distance and 0 <= position_y_gp <= distance:
            valid_data_points += 1

    # angle_blue + angle_green
    position_x_bg = -1
    position_y_bg = -1
    if angle_green is not None and angle_blue is not None:
        h_bg = distance * math.sin(math.radians(angle_blue)) / math.sin(math.radians(angle_green - angle_blue))

        position_x_bg = h_bg * math.cos(math.radians(180 - angle_green))
        position_y_bg = distance - h_bg * math.sin(math.radians(180 - angle_green))
        print("Position from Blue-Green:", position_x_bg, position_y_bg)
        print("")

        if 0 <= position_x_bg <= distance and 0 <= position_y_bg <= distance:
            valid_data_points += 1

    # angle_blue + angle_red
    position_x_br = -1
    position_y_br = -1
    if angle_red is not None and angle_blue is not None:
        h_br = distance * math.sin(math.radians(90 + angle_red)) / math.sin(math.radians(angle_blue - angle_red))

        position_x_br = distance - h_br * math.cos(math.radians(angle_blue))
        position_y_br = distance - h_br * math.sin(math.radians(angle_blue))
        print("Position from Blue-Red:", position_x_br, position_y_br)
        print("")

        if 0 <= position_x_br <= distance and 0 <= position_y_br <= distance:
            valid_data_points += 1

    position_x = None
    position_y = None
    if valid_data_points > 0:
        # Filter out outliers from positions
        threshold = 2
        positions = [(position_x_pr, position_y_pr), (position_x_gp, position_y_gp), (position_x_bg, position_y_bg), (position_x_br, position_y_br)]
        filtered_positions = filter_outliers(positions, threshold)

        # Calculate the averaged position from the filtered positions
        if filtered_positions:
            position_x = sum(pos[0] for pos in filtered_positions) / len(filtered_positions)
            position_y = sum(pos[1] for pos in filtered_positions) / len(filtered_positions)


    x, y, relative_angle = position_x, position_y, relative_angle

    print(f"Position X: {x} Position Y: {y} Angle: {relative_angle}")

    return x, y, relative_angle
