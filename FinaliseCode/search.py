import sys
from collections import deque
import heapq
import numpy as np
from ucs import ucs_search
from Astar import astar
from bfs import bfs_search
from dfs import dfs_search
from gbfs import gbfs
from cus2 import cus2



from Parse_file import parse_file

def main():
    if len(sys.argv) != 3:
        print("Usage: python search_program.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].upper()

    graph, node, origin, destinations  = parse_file(filename)

    if method == "DFS":
        goal, path, nodes_created = dfs_search(graph, origin, destinations)
    elif method == "BFS":
        goal, path, nodes_created = bfs_search(graph, origin, destinations)
    elif method == "ASTAR":
        goal, path, nodes_created = astar(node, graph, origin, destinations)  # A* needs a similar update
    elif method == "GBFS":
         goal, path, nodes_created = gbfs(node, graph, origin, destinations)
    elif method == "CUS1":
        goal, path, nodes_created = ucs_search(graph, origin, destinations)
    elif method == "CUS2":
        goal, path, nodes_created = cus2(node, graph, origin, destinations)
    else:
        print(f"Method '{method}' not implemented. Please choose 'DFS', 'BFS', 'GBFS', 'A*', 'CUS1' or 'CUS2'.")
        sys.exit(1)

    if goal:
        print(f"{method}")
        print(f"{goal} {nodes_created}")
        print(" ".join(path))
    else:
        print(f"NoGoalFound {nodes_created}")
        print("NoPath")

if __name__ == "__main__":
    main()
