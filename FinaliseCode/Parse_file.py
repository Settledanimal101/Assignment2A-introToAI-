import sys
from collections import deque
import heapq
import numpy as np

def parse_file(filename):
    """
    Parses a graph description file containing nodes, edges, origin, and destinations.
    
    Args:
        filename (str): Path to the input file containing graph description
        
    Returns:
        tuple: (graph, node, origin, destinations) where:
            - graph: Dict mapping node IDs to lists of (neighbor, cost) tuples
            - node: Dict mapping node IDs to (x,y) coordinate tuples
            - origin: Starting node ID
            - destinations: List of goal node IDs
    """
    # Initialize data structures
    graph = {}          # Adjacency list representation of the graph
    node = {}           # Dictionary to store node coordinates
    origin = None       # Starting node
    destinations = []   # List of goal nodes

    # Read all lines from file and strip whitespace
    with open(filename, 'r') as f:
        lines = f.read().strip().splitlines()

    # Track current section being parsed
    section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue  # Skip empty lines

        # Determine which section we're parsing
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
            # Parse node format: "node_id: (x,y)"
            node_part, coord_part = line.split(':')
            node_id = node_part.strip()
            # Clean and parse coordinates
            coord_part = coord_part.strip()  # Remove surrounding whitespace
            coords = tuple(map(float, coord_part.strip('() ').split(',')))  # Convert to tuple of floats
            graph[node_id] = []              # Initialize empty adjacency list
            node[node_id] = coords           # Store node coordinates

        elif section == "edges":
            # Parse edge format: "(start,end): cost"
            edge_part, cost_part = line.split(':')
            edge_part = edge_part.strip()
            cost = cost_part.strip()

            # Extract start and end nodes
            edge_part = edge_part.replace('(', '').replace(')', '')
            start_node, end_node = edge_part.split(',')
            start_node = start_node.strip()
            end_node = end_node.strip()

            # Add directed edge to graph
            if start_node not in graph:
                graph[start_node] = []
            graph[start_node].append((end_node, float(cost)))

        elif section == "origin":
            # Parse origin node
            origin = line.strip()

        elif section == "destinations":
            # Parse semicolon-separated destination nodes
            parts = line.split(';')
            for p in parts:
                dest = p.strip()
                if dest:
                    destinations.append(dest)

    return graph, node, origin, destinations
