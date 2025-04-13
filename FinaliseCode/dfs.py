def dfs_search(graph, origin, destinations):
    """
    Implements Depth-First Search to find a path from origin to any destination.
    
    Args:
        graph (dict): Adjacency list representation where each key maps to list of (neighbor, cost) tuples
        origin (str): Starting node ID
        destinations (list): List of possible goal node IDs
    
    Returns:
        tuple: (destination_reached, path, nodes_expanded) where:
            - destination_reached: First destination found (or None if no path exists)
            - path: List of nodes in the solution path
            - nodes_expanded: Number of nodes visited during search
    """
    # Initialize stack with (node, path) pairs - path tracks the route to current node
    stack = [(origin, [origin])]
    
    # Set to track visited nodes and avoid cycles
    visited = set()
    
    # Counter for performance measurement
    nodes_created = 0

    while stack:
        # Pop most recently added node (LIFO order)
        current_node, path_so_far = stack.pop()
        nodes_created += 1

        # Check if we've reached any destination
        if current_node in destinations:
            return current_node, path_so_far, nodes_created

        # Mark current node as visited
        visited.add(current_node)

        if current_node in graph:
            # Get and sort neighbors for consistent tie-breaking
            neighbors = graph[current_node]
            neighbors_sorted = sorted(neighbors, key=lambda x: int(x[0]))
            
            # Process neighbors in reverse order
            # (so they're explored in ascending order due to LIFO stack behavior)
            for (node, _) in reversed(neighbors_sorted):
                if node not in visited:
                    # Create new path by appending neighbor
                    new_path = path_so_far + [node]
                    # Add to stack for later exploration
                    stack.append((node, new_path))

    # No path found to any destination
    return None, [], nodes_created
