import math
import numpy as np

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
pink = (155, 0, 255)

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
            if 0 <= pos[0] <= 8 and 0 <= pos[1] <= 8:  # Add the condition to filter based on valid range
                filtered_positions.append(pos)


    return filtered_positions
