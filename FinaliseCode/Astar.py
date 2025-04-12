import sys
import heapq
import math
from collections import defaultdict
from heuristicFunction import heuristic

def astar(node, graph, origin, destinations):
    frontier = []
    heapq.heappush(frontier, (0, 0, origin, [origin]))  # (f(n), g(n), node, path)
    cost_so_far = {origin: 0}
    visited = set()
    count = 0

    while frontier:
        f, g, current, path = heapq.heappop(frontier)
        
        if current in destinations:
            return current, path, count  # Note the order: goal, path, nodes_created

        if current in visited:
            continue
        visited.add(current)
        count += 1

        for neighbor, edge_cost in sorted(graph[current], key=lambda x: x[0]):
            new_cost = g + edge_cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                # heuristic: take min distance to any goal
                min_h = min(heuristic(node[neighbor], node[goal]) for goal in destinations)
                f_val = new_cost + min_h
                heapq.heappush(frontier, (f_val, new_cost, neighbor, path + [neighbor]))

    return None, [], count  # Again, ordering as (goal, path, nodes_created)
