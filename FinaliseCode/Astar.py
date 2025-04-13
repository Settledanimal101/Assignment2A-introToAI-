import sys
import heapq  # For priority queue implementation
import math
from collections import defaultdict
from heuristicFunction import heuristic  # Custom heuristic function for distance estimation

def astar(node, graph, origin, destinations):
    """
    A* Search Algorithm implementation to find the optimal path from origin to any destination.
    
    Args:
        node (dict): Dictionary of node coordinates {node_id: (x, y)}
        graph (dict): Adjacency list representation of the graph {node_id: [(neighbor_id, cost)]}
        origin (str): Starting node ID
        destinations (list): List of goal node IDs
    
    Returns:
        tuple: (reached_destination, path, nodes_expanded)
            - reached_destination: ID of the destination reached (or None if no path exists)
            - path: List of nodes in the optimal path
            - nodes_expanded: Number of nodes explored during search
    """
    # Initialize priority queue with start node (f_value, g_value, node_id, path)
    frontier = []
    heapq.heappush(frontier, (0, 0, origin, [origin]))  # f=0, g=0 initially

    # Dictionary to keep track of minimum cost to reach each node
    cost_so_far = {origin: 0}
    
    # Set to track visited nodes to avoid cycles
    visited = set()
    
    # Counter for number of nodes expanded
    count = 0

    while frontier:
        # Get node with lowest f-value from priority queue
        # f = g + h where g = cost so far, h = heuristic estimate
        f, g, current, path = heapq.heappop(frontier)
        
        # Skip if node already visited (better path was found)
        if current in visited:
            continue
        visited.add(current)
        
        count += 1  # Increment nodes expanded counter
        
        # Check if current node is a destination
        if current in destinations:
            return current, path, count

        # Explore all neighbors of current node
        for neighbor, edge_cost in sorted(graph[current], key=lambda x: x[0]):
            # Calculate actual cost to reach neighbor through current path
            new_cost = g + edge_cost
            
            # If new path is better than any previous path to this neighbor
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                # Calculate heuristic value (minimum distance to any goal)
                min_h = min(heuristic(node[neighbor], node[goal]) for goal in destinations)
                # f_value = g_value (actual cost) + h_value (heuristic estimate)
                f_val = new_cost + min_h
                # Add neighbor to frontier with updated values
                heapq.heappush(frontier, (f_val, new_cost, neighbor, path + [neighbor]))

    # No path found to any destination
    return None, [], count
