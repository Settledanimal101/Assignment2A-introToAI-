from HeuristicFunction import heuristic

def rbfs_search(graph, origin, destinations, coordinates, f_limit=float('inf')):
    nodes_created = 0  # Count of nodes created

    # Check if the origin is a goal node
    if origin in destinations:
        return origin, [origin], nodes_created

    # Initialize the node information
    successors = graph.get(origin, [])
    best = float('inf')  # Best known cost (f value)
    best_path = None  # Best path to the goal

    for neighbor, edge_cost in successors:
        nodes_created += 1
        g_cost = edge_cost  # Cost from origin to neighbor
        h_cost = heuristic(neighbor, destinations[0], coordinates)  # Heuristic value from neighbor to goal
        f_value = g_cost + h_cost  # Total estimated cost for this neighbor (f = g + h)

        # Recursively explore if the f_value does not exceed the current f_limit
        if f_value <= f_limit:
            result, path, created = rbfs_search(graph, neighbor, destinations, coordinates, min(best, f_value))
            nodes_created += created
            if result is not None:
                # A goal was found; propagate the path back up.
                return result, [origin] + path, nodes_created
            if f_value < best:
                # Update the best known f_value and corresponding path
                best = f_value
                best_path = [origin] + path

    # No valid goal path was found within the cost limit; return the best path encountered.
    return best_path, [], nodes_created
