import math

def triangulation(angle, angle_relative):
    # Define the dimensions of the room in meters
    X = 8
    Y = 8

    positions = []

    # Define the color pairs
    color_pairs = [((0, 0, 255), (255, 0, 255)), ((0, 0, 255), (0, 255, 0)), ((0, 0, 255), (255, 0, 0))]

    for color_pair in color_pairs:
        color1, color2 = color_pair

        # Find alpha and beta
        angle1 = angle.get(color1)
        angle2 = angle.get(color2)
        angle_relative_pair = angle_relative.get((color1, color2))

        if angle1 is None or angle2 is None or angle_relative_pair is None:
            print("Missing angle information for color pair", color_pair)
            continue

        beta = 90 - angle1
        alpha = 180 - beta - angle_relative_pair

        # Find alphap and betap
        angle3 = angle.get((0, 255, 0))
        if angle3 is None:
            print("Missing angle information for color (0, 255, 0)")
            continue

        betap = 90 - angle3
        alphap = 90 - beta

        # Calculate x and y positions
        y = X * math.sin(math.radians(alpha)) * math.sin(math.radians(beta)) / math.sin(math.radians(alpha + beta))
        x = Y * math.sin(math.radians(alphap)) * math.sin(math.radians(betap)) / math.sin(math.radians(alphap + betap))

        positions.append((x, y))

    if len(positions) == 0:
        print("No valid positions calculated")
        return

    # Calculate the average position
    avg_x = sum(p[0] for p in positions) / len(positions)
    avg_y = sum(p[1] for p in positions) / len(positions)

    print("Estimated position:")
    print("x:", avg_x)
    print("y:", avg_y)
