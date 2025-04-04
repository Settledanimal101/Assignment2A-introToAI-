import sys
from collections import deque

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
    origin = None
    destinations = []

    with open(filename, 'r') as f:
        lines = f.read().strip().splitlines()

    # part currently being read
    section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip empty lines

        # Check if we are in a new section
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
            # line: 1: (4,1)
            node_part, _ = line.split(':')
            node_id = node_part.strip()
            if node_id not in graph:
                graph[node_id] = []
        elif section == "edges":
            # line: (2,1): 4
            edge_part, cost_part = line.split(':')
            edge_part = edge_part.strip()   # e.g. (2,1)
            cost = cost_part.strip()        # e.g. 4

            # Remove parentheses and split by comma
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

    return graph, origin, destinations


def dfs_search(graph, origin, destinations):
    # DFS uses a stack. Each item is (current_node, path_so_far)
    stack = [(origin, [origin])]
    visited = set()
    nodes_created = 0

    while stack:
        current_node, path_so_far = stack.pop()
        nodes_created += 1

        if current_node in destinations:
            return current_node, path_so_far, nodes_created

        visited.add(current_node)

        # Get neighbors in ascending order for consistency
        if current_node in graph:
            neighbors = graph[current_node]
            # sort neighbors by integer value of ID and reverse to ensure correct order with stack
            neighbors_sorted = sorted(neighbors, key=lambda x: int(x[0]))
            for (nbr, _) in reversed(neighbors_sorted):
                if nbr not in visited:
                    new_path = path_so_far + [nbr]
                    stack.append((nbr, new_path))

    return None, [], nodes_created


def bfs_search(graph, origin, destinations):
    # Modified BFS that produces the same output format as DFS
    visited = set()
    queue = deque([origin])
    parent = {origin: None}  # For path reconstruction.
    nodes_created = 0

    while queue:
        current = queue.popleft()
        nodes_created += 1

        if current in destinations:
            # Reconstruct the path from origin to the goal
            path = []
            temp = current
            while temp is not None:
                path.append(temp)
                temp = parent[temp]
            path.reverse()
            return current, path, nodes_created

        # Enqueue neighbors not seen before.
        for neighbor, _ in graph.get(current, []):
            if neighbor not in parent:  # ensures it's not already discovered
                parent[neighbor] = current
                queue.append(neighbor)

    return None, [], nodes_created


def main():
    if len(sys.argv) != 3:
        print("Usage: python search_program.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].upper()

    # Parse the file into the graph structure.
    graph, origin, destinations = parse_file(filename)

    print(f"{filename} {method}")
    
    if method == "DFS":
        goal, path, nodes_created = dfs_search(graph, origin, destinations)
        if goal:
            print(f"{goal} {nodes_created}")
            print(" ".join(path))
        else:
            print(f"NoGoalFound {nodes_created}")
            print("NoPath")
    elif method == "BFS":
        goal, path, nodes_created = bfs_search(graph, origin, destinations)
        if goal:
            print(f"{goal} {nodes_created}")
            print(" ".join(path))
        else:
            print(f"NoGoalFound {nodes_created}")
            print("NoPath")
    else:
        print(f"Method '{method}' not implemented. Please choose 'DFS' or 'BFS'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
import sys
from collections import deque

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
    origin = None
    destinations = []

    with open(filename, 'r') as f:
        lines = f.read().strip().splitlines()

    # part currently being read
    section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip empty lines

        # Check if we are in a new section
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
            # line: 1: (4,1)
            node_part, _ = line.split(':')
            node_id = node_part.strip()
            if node_id not in graph:
                graph[node_id] = []
        elif section == "edges":
            # line: (2,1): 4
            edge_part, cost_part = line.split(':')
            edge_part = edge_part.strip()   # e.g. (2,1)
            cost = cost_part.strip()        # e.g. 4

            # Remove parentheses and split by comma
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

    return graph, origin, destinations


def dfs_search(graph, origin, destinations):
    # DFS uses a stack. Each item is (current_node, path_so_far)
    stack = [(origin, [origin])]
    visited = set()
    nodes_created = 0

    while stack:
        current_node, path_so_far = stack.pop()
        nodes_created += 1

        if current_node in destinations:
            return current_node, path_so_far, nodes_created

        visited.add(current_node)

        # Get neighbors in ascending order for consistency
        if current_node in graph:
            neighbors = graph[current_node]
            # sort neighbors by integer value of ID and reverse to ensure correct order with stack
            neighbors_sorted = sorted(neighbors, key=lambda x: int(x[0]))
            for (nbr, _) in reversed(neighbors_sorted):
                if nbr not in visited:
                    new_path = path_so_far + [nbr]
                    stack.append((nbr, new_path))

    return None, [], nodes_created


def bfs_search(graph, origin, destinations):
    # Modified BFS that produces the same output format as DFS
    visited = set()
    queue = deque([origin])
    parent = {origin: None}  # For path reconstruction.
    nodes_created = 0

    while queue:
        current = queue.popleft()
        nodes_created += 1

        if current in destinations:
            # Reconstruct the path from origin to the goal
            path = []
            temp = current
            while temp is not None:
                path.append(temp)
                temp = parent[temp]
            path.reverse()
            return current, path, nodes_created

        # Enqueue neighbors not seen before.
        for neighbor, _ in graph.get(current, []):
            if neighbor not in parent:  # ensures it's not already discovered
                parent[neighbor] = current
                queue.append(neighbor)

    return None, [], nodes_created


def main():
    if len(sys.argv) != 3:
        print("Usage: python search_program.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2].upper()

    # Parse the file into the graph structure.
    graph, origin, destinations = parse_file(filename)

    print(f"{filename} {method}")
    
    if method == "DFS":
        goal, path, nodes_created = dfs_search(graph, origin, destinations)
        if goal:
            print(f"{goal} {nodes_created}")
            print(" ".join(path))
        else:
            print(f"NoGoalFound {nodes_created}")
            print("NoPath")
    elif method == "BFS":
        goal, path, nodes_created = bfs_search(graph, origin, destinations)
        if goal:
            print(f"{goal} {nodes_created}")
            print(" ".join(path))
        else:
            print(f"NoGoalFound {nodes_created}")
            print("NoPath")
    else:
        print(f"Method '{method}' not implemented. Please choose 'DFS' or 'BFS'.")
        sys.exit(1)


if __name__ == "__main__":
    main()