import math
import cmath

def filter_outliers(positions, threshold):
    # Calculate the mean position
    mean_x = sum(pos[0] for pos in positions) / len(positions)
    mean_y = sum(pos[1] for pos in positions) / len(positions)

    # Calculate the standard deviation of positions
    std_x = math.sqrt(sum((pos[0] - mean_x) ** 2 for pos in positions) / len(positions))
    std_y = math.sqrt(sum((pos[1] - mean_y) ** 2 for pos in positions) / len(positions))

    # Filter out positions that deviate beyond the threshold
    filtered_positions = []
    for pos in positions:
        if abs(pos[0] - mean_x) <= threshold * std_x and abs(pos[1] - mean_y) <= threshold * std_y:
            filtered_positions.append(pos)

    return filtered_positions

def calculate_robot_angle(position_x, position_y, angle_red, angle_green, angle_blue, angle_pink):
    # Calculate the angle between the robot and a reference axis (such as the x-axis)

    # Convert the angle values to radians
    angle_red_rad = math.radians(angle_red)
    angle_green_rad = math.radians(angle_green)
    angle_blue_rad = math.radians(angle_blue)
    angle_pink_rad = math.radians(angle_pink)

    # Set the distances between colors
    distance_rg = 8
    distance_gb = 8
    distance_bp = 8
    distance_pr = 8

    # Calculate the relative angles between the colors
    if angle_green is None:
        relative_angle_rg = None
    else:
        relative_angle_rg = angle_green_rad - angle_red_rad

    if angle_blue is None:
        relative_angle_gb = None
    else:
        relative_angle_gb = angle_blue_rad - angle_green_rad

    if angle_pink is None:
        relative_angle_bp = None
    else:
        relative_angle_bp = angle_pink_rad - angle_blue_rad

    if angle_red is None:
        relative_angle_pr = None
    else:
        relative_angle_pr = angle_red_rad - angle_pink_rad

    # Calculate the positions of the colors relative to the robot's position
    if relative_angle_rg is not None:
        position_rg = complex(position_x, position_y) + cmath.rect(distance_rg, angle_red_rad)
    else:
        position_rg = None

    if relative_angle_gb is not None:
        position_gb = complex(position_x, position_y) + cmath.rect(distance_gb, angle_green_rad)
    else:
        position_gb = None

    if relative_angle_bp is not None:
        position_bp = complex(position_x, position_y) + cmath.rect(distance_bp, angle_blue_rad)
    else:
        position_bp = None

    if relative_angle_pr is not None:
        position_pr = complex(position_x, position_y) + cmath.rect(distance_pr, angle_pink_rad)
    else:
        position_pr = None

    # Calculate the centroid of the available color positions
    positions = [pos for pos in [position_rg, position_gb, position_bp, position_pr] if pos is not None]
    if positions:
        centroid = sum(positions) / len(positions)
    else:
        centroid = None

    # Calculate the angle between the robot's position and the centroid if available
    if centroid is not None:
        robot_angle_rad = cmath.phase(centroid - complex(position_x, position_y))
        robot_angle_deg = math.degrees(robot_angle_rad)
    else:
        robot_angle_deg = None

    return robot_angle_deg
