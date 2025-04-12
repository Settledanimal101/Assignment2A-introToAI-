import sys
from collections import deque
import heapq
import numpy as np
from bfs import bfs_search
from dfs import dfs_search
from gbfs import GBFS_search
from Astar import Astar_search
from ucs import ucs_search
from cus2 import rbfs_search

from Parse_file import parse_file

def main():
    if len(sys.argv) != 3:
        print("Usage: python search_program.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].upper()

    graph, coordinates, origin, destinations = parse_file(filename)

    if method == "DFS":
        goal, path, nodes_created = dfs_search(graph, origin, destinations)
    elif method == "BFS":
        goal, path, nodes_created = bfs_search(graph, origin, destinations)
    elif method == "GBFS":
        goal, path, nodes_created = GBFS_search(graph, origin, destinations, coordinates)
    elif method == "ASTAR":
        goal, path, nodes_created = Astar_search(graph, origin, destinations, coordinates)  # A* needs a similar update
    elif method == "CUS1":
        goal, path, nodes_created = ucs_search(graph, origin, destinations)
    elif method == "CUS2":
        goal, path, nodes_created = rbfs_search(graph, origin, destinations, coordinates)
    else:
        print(f"Method '{method}' not implemented. Please choose 'DFS', 'BFS', 'GBFS', 'A*', 'CUS1' or 'CUS2'.")
        sys.exit(1)

    if goal:
        print(f"{goal} {nodes_created}")
        print(" ".join(path))
    elif coordinates:
        print("Node not found")
    else:
        print(f"NoGoalFound {nodes_created}")
        print("NoPath")

if __name__ == "__main__":
    main()