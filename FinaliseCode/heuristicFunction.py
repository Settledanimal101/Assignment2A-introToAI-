import math

def heuristic(coord1, coord2):
    return math.hypot(coord1[0] - coord2[0], coord1[1] - coord2[1])