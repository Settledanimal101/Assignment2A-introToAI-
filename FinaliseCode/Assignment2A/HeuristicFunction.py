import sys
from collections import deque
import heapq
import numpy as np
def heuristic(current_node, goal_node, coordinates):
    # Check if the goal node exists; if not, return an error message.
    if goal_node not in coordinates:
        return None

    current_coords = coordinates[current_node]
    goal_coords = coordinates[goal_node]
    
    return np.sqrt((current_coords[0] - goal_coords[0]) ** 2 + (current_coords[1] - goal_coords[1]) ** 2)

