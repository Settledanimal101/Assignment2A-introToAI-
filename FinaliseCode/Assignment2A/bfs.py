from collections import deque

def bfs_search(graph, origin, destinations):
    # Initialize a set of visited nodes and a queue for BFS
    visited = set([origin])
    queue = deque([origin])
    
    # Dictionary to trace parents for path reconstruction
    parent = {origin: None}
    
    # Counter to track the number of nodes expanded during the search
    nodes_created = 0

    # Continue processing until the queue is empty (i.e., all reachable nodes are explored)
    while queue:
        # Dequeue the node at the front of the queue
        current = queue.popleft()
        nodes_created += 1

        # If the current node is in the set of destination nodes,
        # reconstruct the path from origin to the current node.
        if current in destinations:
            path = []
            temp = current
            # Trace back using parent pointers
            while temp is not None:
                path.append(temp)
                temp = parent[temp]
            path.reverse()  # Reverse the path to get the correct order from origin to destination
            return current, path, nodes_created

        # Explore neighbors in sorted order based on node value (converted to integer)
        # Note: The cost value is ignored for BFS.
        for neighbor, _ in sorted(graph.get(current, []), key=lambda x: int(x[0])):
            if neighbor not in visited:
                # Mark neighbor as visited to prevent revisiting
                visited.add(neighbor)
                # Set the current node as the parent of the neighbor (for path reconstruction)
                parent[neighbor] = current
                # Enqueue the neighbor
                queue.append(neighbor)

    # If the queue is exhausted and no destination is found, return failure result
    return None, [], nodes_created