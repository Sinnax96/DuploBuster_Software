def triangulation():
    # Define the dimensions of the room in meters
    X = 8
    Y = 8

    # Angle between corner
    # Compute the angle between each line
    angles_lines = {}
    colors = list(polar_coords.keys())
    for i in range(len(colors)):
        for j in range(i+1, len(colors)):
            color1, color2 = colors[i], colors[j]
            polar_coord1, polar_coord2 = polar_coords[color1], polar_coords[color2]
            polar_theta1, polar_theta2 = polar_coord1[1], polar_coord2[1]
            angle_deg = abs(np.rad2deg(polar_theta2 - polar_theta1))
            angles_lines[(color1, color2)] = angle_deg
            print(f"The angle between the {color1} and {color2} lines is {angle_deg:.2f} degrees.")

    # Find alpha and beta
    beta = 90 - angles[(0, 0, 255)]
    alpha = 180 - beta - angles_lines[(0, 0, 255), (255, 192, 203)]

    # Find alphap and betap
    betap = 90 - angles[(0, 255, 0)]
    alphap = 90 - beta

    # x,y position
    y = X * math.sin(alpha) * math.sin(beta) / math.sin(alpha+beta)
    x = Y * math.sin(alphap) * math.sin(betap) / math.sin(alphap+betap)

    print(y)
    print(x)
