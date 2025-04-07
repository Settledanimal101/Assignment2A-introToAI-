import sys
from collections import deque
import heapq
import numpy as np

import sys
from collections import deque
import heapq
import numpy as np

def parse_file(filename):
    """
    Reads a text file describing:
      - Nodes with coordinates
      - Edges with costs (directed)
      - Origin node
      - Destination nodes
    Then builds an adjacency list for the graph and returns (graph, origin, destinations).
    """
    graph = {}
    coordinates = {}
    origin = None
    destinations = []

    with open(filename, 'r') as f:
        lines = f.read().strip().splitlines()

    section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip empty lines

        if line.startswith("Nodes:"):
            section = "nodes"
            continue
        elif line.startswith("Edges:"):
            section = "edges"
            continue
        elif line.startswith("Origin:"):
            section = "origin"
            continue
        elif line.startswith("Destinations:"):
            section = "destinations"
            continue

        if section == "nodes":
            node_part, coord_part = line.split(':')
            node_id = node_part.strip()
            # Cleaning the coordinates part
            coord_part = coord_part.strip()  # Remove any surrounding whitespace
            coords = tuple(map(float, coord_part.strip('() ').split(',')))  # Remove parentheses and spaces
            graph[node_id] = []
            coordinates[node_id] = coords  # Store the coordinates
        elif section == "edges":
            edge_part, cost_part = line.split(':')
            edge_part = edge_part.strip()
            cost = cost_part.strip()

            edge_part = edge_part.replace('(', '').replace(')', '')
            start_node, end_node = edge_part.split(',')
            start_node = start_node.strip()
            end_node = end_node.strip()

            if start_node not in graph:
                graph[start_node] = []
            graph[start_node].append((end_node, float(cost)))
        elif section == "origin":
            origin = line.strip()
        elif section == "destinations":
            parts = line.split(';')
            for p in parts:
                dest = p.strip()
                if dest:
                    destinations.append(dest)

    return graph, coordinates, origin, destinations 


def heuristic(current_node, goal_node, coordinates):
    # Check if the goal node exists; if not, return an error message.
    if goal_node not in coordinates:
        return None

    current_coords = coordinates[current_node]
    goal_coords = coordinates[goal_node]
    
    return np.sqrt((current_coords[0] - goal_coords[0]) ** 2 + (current_coords[1] - goal_coords[1]) ** 2)


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
                priority = new_cost + heuristic(neighbor, destinations[0], coordinates)
                new_path = path_so_far + [neighbor]
                heapq.heappush(priority_queue, (priority, neighbor, new_path))

    return None, [], nodes_created  # If no path is found
