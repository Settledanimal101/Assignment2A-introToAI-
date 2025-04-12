import sys
from collections import deque
import heapq
import numpy as np

def parse_file(filename):
  
    graph = {}
    node = {}
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
            node[node_id] = coords  # Store the coordinates
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

    return graph, node, origin, destinations 
