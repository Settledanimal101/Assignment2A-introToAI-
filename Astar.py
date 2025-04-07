import sys
import heapq
import math
from collections import defaultdict

def parse_file(filename):
    nodes = {}
    edges = defaultdict(list)
    origin = None
    destinations = []

    with open(filename, 'r') as f:
        lines = f.readlines()

    section = None
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line or line.startswith('#'):
            continue

        if line.startswith('Nodes:'):
            section = 'nodes'
            continue
        elif line.startswith('Edges:'):
            section = 'edges'
            continue
        elif line.startswith('Origin:'):
            section = 'origin'
            if i < len(lines):
                origin = int(lines[i].strip())
                i += 1
            continue
        elif line.startswith('Destinations:'):
            section = 'destinations'
            if i < len(lines):
                destinations = list(map(int, lines[i].strip().split(';')))
                i += 1
            continue

        if section == 'nodes':
            nid, coord = line.split(':')
            x, y = eval(coord.strip())
            nodes[int(nid.strip())] = (x, y)
        elif section == 'edges':
            edge_part, cost = line.split(':')
            from_node, to_node = eval(edge_part.strip())
            edges[from_node].append((to_node, int(cost.strip())))

    return nodes, edges, origin, destinations

def heuristic(coord1, coord2):
    return math.hypot(coord1[0] - coord2[0], coord1[1] - coord2[1])

def astar(nodes, edges, start, goals):
    frontier = []
    heapq.heappush(frontier, (0, 0, start, [start]))  # (f(n), g(n), node, path)
    cost_so_far = {start: 0}
    visited = set()
    count = 0

    while frontier:
        f, g, current, path = heapq.heappop(frontier)
        

        if current in goals:
            return current, count, path

        if current in visited:
            continue
        visited.add(current)
        count += 1

        for neighbor, edge_cost in sorted(edges[current], key=lambda x: x[0]):
            new_cost = g + edge_cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                # heuristic: take min distance to any goal
                min_h = min(heuristic(nodes[neighbor], nodes[goal]) for goal in goals)
                f_val = new_cost + min_h
                heapq.heappush(frontier, (f_val, new_cost, neighbor, path + [neighbor]))

    return None, count, []

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python AS.py <filename> AS")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2]

    if method != 'AS':
        print("Only 'AS' method is supported in this script.")
        sys.exit(1)

    nodes, edges, origin, destinations = parse_file(filename)
    goal, created, path = astar(nodes, edges, origin, destinations)

    print(f"{filename} {method}")
    if goal:
        print(goal, created)
        print(" ".join(map(str, path)))
    else:
        print("No path found.")
