import heapq
from heuristicFunction import heuristic

def cus2(node, graph, origin, destinations, weight=1.5):
   
    visited = set()
    queue = []

    # Compute initial heuristic as the minimum over all destination nodes.
    initial_h = min(heuristic(node[origin], node[d]) for d in destinations)
    heapq.heappush(queue, (initial_h * weight, 0, origin, [origin]))  # (f, g, node, path)

    while queue:
        f, g, current, path = heapq.heappop(queue)

        if current in visited:
            continue
        visited.add(current)

        if current in destinations:
            return current, path, len(visited)

        # Process neighbors; assuming graph[current] returns [(neighbor, cost), ...].
        neighbors = sorted(graph.get(current, []), key=lambda x: x[0])
        for neighbor, cost in neighbors:
            if neighbor not in visited:
                g_new = g + cost
                h_new = min(heuristic(node[neighbor], node[d]) for d in destinations)
                f_new = g_new + weight * h_new
                heapq.heappush(queue, (f_new, g_new, neighbor, path + [neighbor]))

    return None, [], len(visited)
