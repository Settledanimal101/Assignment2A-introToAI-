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


def dfs_search(graph, origin, destinations):
    stack = [(origin, [origin])]
    visited = set()
    nodes_created = 0

    while stack:
        current_node, path_so_far = stack.pop()
        nodes_created += 1

        if current_node in destinations:
            return current_node, path_so_far, nodes_created

        visited.add(current_node)

        if current_node in graph:
            neighbors = graph[current_node]
            neighbors_sorted = sorted(neighbors, key=lambda x: int(x[0]))
            for (nbr, _) in reversed(neighbors_sorted):
                if nbr not in visited:
                    new_path = path_so_far + [nbr]
                    stack.append((nbr, new_path))

    return None, [], nodes_created


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
                priority = heuristic(neighbor_node, list(destinations)[0], coordinates)
                
                # Update path for the neighbor by extending from the current path
                new_path = path_so_far + [neighbor_node]
                
                # Push the neighbor with its computed priority onto the priority queue
                heapq.heappush(priority_queue, (priority, neighbor_node, new_path))

    # If no destination is reached, return failure with an empty path
    return None, [], nodes_created

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


def ucs_search(graph, origin, destinations):
    """
    Perform Uniform Cost Search (UCS) on a weighted graph to find the least-cost
    path from the origin to one of the destination nodes.
    
    UCS is an uninformed search algorithm that expands the node with the lowest 
    cumulative cost first. This implementation uses a priority queue (min-heap) 
    to always select the node with the smallest cost.
    """
     # Initialize the priority queue with a tuple (cumulative_cost, current_node, path_so_far)
    # Start with the origin node and a cumulative cost of 0.
    priority_queue = [(0, origin, [origin])]
    
    # A set to keep track of visited nodes so we don't process them again
    visited = set()
    
    # Counter for the number of nodes expanded during the search
    nodes_created = 0

    # Continue the search until there are no nodes left in the priority queue
    while priority_queue:
        # Pop the node with the smallest cumulative cost from the queue
        cost, current_node, path_so_far = heapq.heappop(priority_queue)
        nodes_created += 1  # Increment each time a node is expanded
        
        # Check if the current node is one of the destination nodes
        if current_node in destinations:
            return current_node, path_so_far, nodes_created
        
        # Mark the current node as visited
        visited.add(current_node)

        # Loop through all neighbors of the current node from the graph
        for neighbor, edge_cost in graph.get(current_node, []):
            # Only consider neighbors that haven't been visited
            if neighbor not in visited:
                # Calculate the new cumulative cost to reach this neighbor
                new_cost = cost + edge_cost
                # Create a new path by appending the neighbor node to the current path
                new_path = path_so_far + [neighbor]
                # Push the new state (cost, neighbor, new_path) to the priority queue
                heapq.heappush(priority_queue, (new_cost, neighbor, new_path))

    # If the priority queue is exhausted without reaching a destination, return failure
    return None, [], nodes_created

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



def main():
    if len(sys.argv) != 3:
        print("Usage: python search_program.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].upper()

    graph, coordinates, origin, destinations = parse_file(filename)

    if method == "DFS":
        goal, path, nodes_created = dfs_search(graph, origin, destinations)
    elif method == "BFS":
        goal, path, nodes_created = bfs_search(graph, origin, destinations)
    elif method == "GBFS":
        goal, path, nodes_created = GBFS_search(graph, origin, destinations, coordinates)
    elif method == "ASTAR":
        goal, path, nodes_created = Astar_search(graph, origin, destinations, coordinates)  # A* needs a similar update
    elif method == "CUS1":
        goal, path, nodes_created = ucs_search(graph, origin, destinations)
    elif method == "CUS2":
        goal, path, nodes_created = rbfs_search(graph, origin, destinations, coordinates)
    else:
        print(f"Method '{method}' not implemented. Please choose 'DFS', 'BFS', 'GBFS', 'A*', 'CUS1' or 'CUS2'.")
        sys.exit(1)

    if goal:
        print(f"{goal} {nodes_created}")
        print(" ".join(path))
    elif coordinates:
        print("Node not found")
    else:
        print(f"NoGoalFound {nodes_created}")
        print("NoPath")

if __name__ == "__main__":
    main()
