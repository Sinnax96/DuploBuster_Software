import math

def triangulation(angle, angle_relative):
    # Define the dimensions of the room in meters
    X = 8
    Y = 8

    # Find alpha and beta
    beta = 90 - angle[(0, 0, 255)]
    alpha = 180 - beta - angle_relative[(0, 0, 255), (255, 192, 203)]

    # Find alphap and betap
    betap = 90 - angle[(0, 255, 0)]
    alphap = 90 - beta

    # x,y position
    y = X * math.sin(alpha) * math.sin(beta) / math.sin(alpha+beta)
    x = Y * math.sin(alphap) * math.sin(betap) / math.sin(alphap+betap)

    print(y)
    print(x)
