import numpy as np

def angles_polar(polar_coords):
    # Compute the angle of each line
    angles = {}
    for i, polar_coord in enumerate(polar_coords):
        polar_r, polar_theta = polar_coord
        angle_deg = np.rad2deg(polar_theta)
        angles[i] = angle_deg
        print(f"The angle of the {i+1}-th line is {angle_deg:.2f} degrees.")
    return angles
