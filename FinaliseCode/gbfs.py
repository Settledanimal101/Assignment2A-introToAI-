import heapq
import math
from heuristicFunction import heuristic

def gbfs(node, graph, origin, destinations):
    """
    Implements Greedy Best-First Search to find a path from origin to any destination.
    Uses straight-line distance heuristic to guide the search.
    
    Args:
        node (dict): Dictionary mapping node IDs to (x,y) coordinates
        graph (dict): Adjacency list representation {node: [(neighbor, cost)]}
        origin (str): Starting node ID
        destinations (list): List of possible goal node IDs
    
    Returns:
        tuple: (destination_reached, path, nodes_expanded) where:
            - destination_reached: First destination found (or None if no path exists)
            - path: List of nodes in the solution path
            - nodes_expanded: Number of nodes visited during search
    """
    # Initialize set to track visited nodes and avoid cycles
    visited = set()
    nodes_created = 0  # Count of nodes expanded
    
    # Priority queue stores tuples: (heuristic_value, node_id, path_to_node)
    queue = []

    # Calculate initial heuristic value (distance to closest destination)
    initial_h = min(heuristic(node[origin], node[g]) for g in destinations)
    heapq.heappush(queue, (initial_h, origin, [origin]))

    while queue:
        # Get node with lowest heuristic value from priority queue
        curr_priority, current, path = heapq.heappop(queue)
        
        # Skip if already visited (better path was found)
        if current in visited:
            continue

        # Mark node as visited and increment expansion counter
        visited.add(current)
        nodes_created += 1

        # Check if we've reached one of the destinations
        if current in destinations:
            return current, path, nodes_created

        # Process neighbors in sorted order for consistent tie-breaking
        neighbors = sorted(graph.get(current, []), key=lambda x: x[0])
        for neighbor, _ in neighbors:
            if neighbor not in visited:
                # Calculate heuristic value for neighbor (distance to closest goal)
                new_h = min(heuristic(node[neighbor], node[g]) for g in destinations)
                # Add to queue with heuristic as priority
                heapq.heappush(queue, (new_h, neighbor, path + [neighbor]))

    # Return None if no path is found to any destination
    return None, [], nodes_created
