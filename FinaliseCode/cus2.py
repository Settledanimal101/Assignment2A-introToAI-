import heapq
from heuristicFunction import heuristic

def cus2(node, graph, origin, destinations, weight=1.5):
    """
    Custom search algorithm combining aspects of A* with weighted heuristics.
    Similar to Weighted A* but with modified heuristic influence.
    
    Args:
        node (dict): Dictionary mapping node IDs to (x,y) coordinates
        graph (dict): Adjacency list representation of the graph {node: [(neighbor, cost)]}
        origin (str): Starting node ID
        destinations (list): List of possible goal node IDs
        weight (float): Heuristic weight factor (default=1.5) to control search greediness
    
    Returns:
        tuple: (goal_node, path, nodes_expanded) where:
            - goal_node: First destination reached (or None if no path exists)
            - path: List of nodes in the solution path
            - nodes_expanded: Number of nodes visited during search
    """
    # Initialize closed set for visited nodes
    visited = set()
    
    # Priority queue for open set: (f_value, g_value, node_id, path)
    queue = []

    # Calculate initial heuristic value (minimum distance to any goal)
    initial_h = min(heuristic(node[origin], node[d]) for d in destinations)
    # Push start node with weighted heuristic value
    heapq.heappush(queue, (initial_h * weight, 0, origin, [origin]))

    while queue:
        # Get node with lowest f-value (f = g + weight*h)
        f, g, current, path = heapq.heappop(queue)

        # Skip if already visited (better path was found)
        if current in visited:
            continue
        visited.add(current)

        # Check if we've reached any destination
        if current in destinations:
            return current, path, len(visited)

        # Process neighbors in sorted order for consistent tie-breaking
        neighbors = sorted(graph.get(current, []), key=lambda x: x[0])
        for neighbor, cost in neighbors:
            if neighbor not in visited:
                # Calculate new path cost to neighbor
                g_new = g + cost
                # Calculate heuristic estimate to closest goal
                h_new = min(heuristic(node[neighbor], node[d]) for d in destinations)
                # Calculate f-value with weighted heuristic
                f_new = g_new + weight * h_new
                # Add neighbor to queue with updated values
                heapq.heappush(queue, (f_new, g_new, neighbor, path + [neighbor]))

    # No path found to any destination
    return None, [], len(visited)
