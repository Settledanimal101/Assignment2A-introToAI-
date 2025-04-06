def ucs_search(graph, origin, destinations):
    """
    Perform Uniform Cost Search (UCS) on a weighted graph to find the least-cost
    path from the origin to one of the destination nodes.
    
    UCS is an uninformed search algorithm that expands the node with the lowest 
    cumulative cost first. This implementation uses a priority queue (min-heap) 
    to always select the node with the smallest cost.
    """
     # Initialize the priority queue with a tuple (cumulative_cost, current_node, path_so_far)
    # Start with the origin node and a cumulative cost of 0.
    priority_queue = [(0, origin, [origin])]
    
    # A set to keep track of visited nodes so we don't process them again
    visited = set()
    
    # Counter for the number of nodes expanded during the search
    nodes_created = 0

    # Continue the search until there are no nodes left in the priority queue
    while priority_queue:
        # Pop the node with the smallest cumulative cost from the queue
        cost, current_node, path_so_far = heapq.heappop(priority_queue)
        nodes_created += 1  # Increment each time a node is expanded
        
        # Check if the current node is one of the destination nodes
        if current_node in destinations:
            return current_node, path_so_far, nodes_created
        
        # Mark the current node as visited
        visited.add(current_node)

        # Loop through all neighbors of the current node from the graph
        for neighbor, edge_cost in graph.get(current_node, []):
            # Only consider neighbors that haven't been visited
            if neighbor not in visited:
                # Calculate the new cumulative cost to reach this neighbor
                new_cost = cost + edge_cost
                # Create a new path by appending the neighbor node to the current path
                new_path = path_so_far + [neighbor]
                # Push the new state (cost, neighbor, new_path) to the priority queue
                heapq.heappush(priority_queue, (new_cost, neighbor, new_path))

    # If the priority queue is exhausted without reaching a destination, return failure
    return None, [], nodes_created
