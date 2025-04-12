import heapq
import math
from heuristicFunction import heuristic

def gbfs(node, graph, origin, destinations):
    visited = set()
    nodes_created = 0  # Count of nodes expanded
    queue = []

    # Initial state: compute heuristic from origin to the closest destination
    initial_h = min(heuristic(node[origin], node[g]) for g in destinations)
    heapq.heappush(queue, (initial_h, origin, [origin]))

    while queue:
        curr_priority, current, path = heapq.heappop(queue)
        
        # Skip if already visited
        if current in visited:
            continue

        visited.add(current)
        nodes_created += 1

        # Check if we've reached one of the destinations
        if current in destinations:
            return current, path, nodes_created

        # Process neighbors; assuming graph[current] returns a list of (neighbor, cost) pairs.
        neighbors = sorted(graph.get(current, []), key=lambda x: x[0])
        for neighbor, _ in neighbors:
            if neighbor not in visited:
                new_h = min(heuristic(node[neighbor], node[g]) for g in destinations)
                heapq.heappush(queue, (new_h, neighbor, path + [neighbor]))

    # If no path is found
    return None, [], nodes_created
