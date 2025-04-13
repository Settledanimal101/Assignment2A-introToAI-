from collections import deque

def bfs_search(graph, origin, destinations):
    """
    Performs Breadth-First Search to find the shortest unweighted path from origin to any destination.
    
    Args:
        graph (dict): Adjacency list representation where each key maps to list of (neighbor, cost) tuples
        origin (str): Starting node ID
        destinations (list): List of goal node IDs
    
    Returns:
        tuple: (destination_reached, path, nodes_expanded) where:
            - destination_reached: First destination found or None if no path exists
            - path: List of nodes in order from origin to destination
            - nodes_expanded: Number of nodes explored during search
    """
    # Initialize data structures for BFS
    visited = set([origin])      # Track visited nodes to avoid cycles
    queue = deque([origin])      # FIFO queue for BFS node expansion
    parent = {origin: None}      # Store parent pointers for path reconstruction
    nodes_created = 0            # Counter for performance tracking

    while queue:
        # Get next node from front of queue (FIFO order ensures shortest path)
        current = queue.popleft()
        nodes_created += 1

        # Check if we've reached any destination
        if current in destinations:
            # Reconstruct path by following parent pointers backwards
            path = []
            temp = current
            while temp is not None:
                path.append(temp)
                temp = parent[temp]
            path.reverse()  # Convert from destination->origin to origin->destination
            return current, path, nodes_created

        # Process all unvisited neighbors
        # Sort neighbors by ID for consistent tie-breaking
        for neighbor, _ in sorted(graph.get(current, []), key=lambda x: int(x[0])):
            if neighbor not in visited:
                visited.add(neighbor)          # Mark as visited
                parent[neighbor] = current     # Record how we reached this node
                queue.append(neighbor)         # Add to queue for later expansion

    # No path found to any destination
    return None, [], nodes_created