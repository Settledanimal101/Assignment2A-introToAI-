import heapq
from HeuristicFunction import heuristic

def GBFS_search(graph, origin, destinations, coordinates):
   # Initialize the priority queue with a tuple: (priority, node, path)
    priority_queue = []
    heapq.heappush(priority_queue, (0, origin, [origin]))
    
    # Set to keep track of visited nodes
    visited = set()
    
    # Counter for number of nodes processed (expanded)
    nodes_created = 0

    # Process nodes until the priority queue is empty (i.e., all reachable nodes processed)
    while priority_queue:
        # Pop the node with the smallest heuristic value from the queue
        _, current_node, path_so_far = heapq.heappop(priority_queue)
        nodes_created += 1

        # Check if the current node is one of the destination nodes
        if current_node in destinations:
            return current_node, path_so_far, nodes_created

        # Mark the current node as visited to avoid reprocessing it later
        visited.add(current_node)

        # Examine neighbors of the current node
        for neighbor in graph.get(current_node, []):
            neighbor_node = neighbor[0]  # Extract the neighbor node from the edge tuple
            if neighbor_node not in visited:
                # Calculate the priority (heuristic value) for the neighbor node
                # Here, the heuristic function is applied using this neighbor,
                # one of the destination nodes (destinations[0]), and coordinates.
                priority = float('inf')
                for node in destinations:
                    new_priority = heuristic(neighbor_node, node, coordinates)
                    if new_priority < priority:
                        priority = new_priority

                
                # Update path for the neighbor by extending from the current path
                new_path = path_so_far + [neighbor_node]
                
                # Push the neighbor with its computed priority onto the priority queue
                heapq.heappush(priority_queue, (priority, neighbor_node, new_path))

    # If no destination is reached, return failure with an empty path
    return None, [], nodes_created