def ucs_search(graph, origin, destinations):
    # Initialize the priority queue with tuples in the order: (cumulative_cost, current_node, path)
    frontier = [(0, origin, [origin])]
    
    # A set to keep track of visited nodes so we don't process them again
    visited = set()
    
    # Counter for the number of nodes expanded during the search
    nodes_created = 0

    while frontier:
        # Pop the node with the smallest cumulative cost from the queue
        cost, current, path = heapq.heappop(frontier)
        nodes_created += 1  # Increment each time a node is expanded
        
        # Check if the current node is one of the destination nodes
        if current in destinations:
            return current, path, nodes_created

        if current in visited:
            continue
        visited.add(current)

        for neighbor, edge_cost in graph.get(current, []):
            if neighbor not in visited:
                total_cost = cost + edge_cost
                # Add neighbor to the queue with updated cost and path
                heapq.heappush(frontier, (total_cost, neighbor, path + [neighbor]))

    return None, [], nodes_created
