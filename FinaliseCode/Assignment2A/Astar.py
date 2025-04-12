import sys
import heapq
from HeuristicFunction import heuristic

def Astar_search(graph, origin, destinations, coordinates):
    priority_queue = []
    # Keep track of the total cost from the start node to the current node and the heuristic cost
    heapq.heappush(priority_queue, (0, origin, [origin]))  # (total_cost, node, path)
    visited = set()  # Keep track of visited nodes
    cost_so_far = {origin: 0}  # G-cost of paths to reach each node
    nodes_created = 0

    while priority_queue:
        total_cost, current_node, path_so_far = heapq.heappop(priority_queue)
        nodes_created += 1

        if current_node in destinations:
            return current_node, path_so_far, nodes_created

        visited.add(current_node)

        for neighbor, edge_cost in graph.get(current_node, []):
            if neighbor in visited:
                continue  # Skip already visited nodes

            new_cost = cost_so_far[current_node] + edge_cost  # Cost from start to this neighbor

            # Update cost_so_far if it's not recorded yet or if we found a cheaper way
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                # Use the heuristic to guide the search
                priority = float('inf')
                for node in destinations:
                    new_priority = new_cost + heuristic(neighbor, node, coordinates)
                    if new_priority < priority:
                        priority = new_priority
                    
                    

                new_path = path_so_far + [neighbor]
                heapq.heappush(priority_queue, (priority, neighbor, new_path))

    return None, [], nodes_created  # If no path is found