import sys

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

    # Track which section of the file we're currently reading
    section = None

    for line in lines:
        line = line.strip()

        if not line:
            continue  # skip empty lines

        # Check if the line signals a new section
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
            # Example line: 1: (4,1)
            # We don't strictly need the coordinates for DFS, but let's parse them anyway
            node_part, coord_part = line.split(':')
            node_id = node_part.strip()
            # coords in the form (x,y)
            # (We won't use these for DFS, but let's parse them to illustrate how it works)
            _coords = coord_part.strip()

            # Initialize adjacency list for this node if not present
            if node_id not in graph:
                graph[node_id] = []

        elif section == "edges":
            # Example line: (2,1): 4
            # meaning an edge from node 2 to node 1 with cost 4
            edge_part, cost_part = line.split(':')
            edge_part = edge_part.strip()  # e.g. (2,1)
            cost = cost_part.strip()       # e.g. 4

            # Remove parentheses, split on comma
            edge_part = edge_part.replace('(', '').replace(')', '')
            start_node, end_node = edge_part.split(',')
            start_node = start_node.strip()
            end_node   = end_node.strip()

            # Insert into adjacency list
            if start_node not in graph:
                graph[start_node] = []
            graph[start_node].append((end_node, float(cost)))

        elif section == "origin":
            # single line, e.g. 2
            origin = line.strip()

        elif section == "destinations":
            # may be multiple destinations, separated by semicolons
            # e.g. 5; 4
            parts = line.split(';')
            for p in parts:
                dest = p.strip()
                if dest:
                    destinations.append(dest)

    return graph, origin, destinations


def dfs_search(graph, origin, destinations):
    """
    Performs a Depth-First Search on the given graph from 'origin' to find
    any of the 'destinations'. Returns (found_destination, path, nodes_created).

    - graph is a dict: { node: [(neighbor, cost), ...], ... }
    - origin is the start node
    - destinations is a list of goal nodes
    """

    # We'll use a stack for DFS. Each item on the stack is a tuple:
    # (current_node, path_to_here)
    stack = [(origin, [origin])]
    visited = set()        # keep track of visited nodes to avoid cycles
    nodes_created = 0      # how many nodes we've generated/expanded so far

    while stack:
        current_node, path_so_far = stack.pop()
        nodes_created += 1  # we've taken one node off the stack (expanded it)

        # If we have reached a destination, return success immediately
        if current_node in destinations:
            return current_node, path_so_far, nodes_created

        # Mark current node as visited
        visited.add(current_node)

        # Get neighbors in ascending order of node ID if you want consistent tie-breaking
        # e.g., sorted by neighbor ID (string comparison or int conversion)
        if current_node in graph:
            neighbors = graph[current_node]
            # neighbors is a list of (neighbor_id, cost)
            # We'll sort by neighbor_id as an integer to match "ascending order" if needed
            neighbors_sorted = sorted(neighbors, key=lambda x: int(x[0]))

            for (nbr, _) in reversed(neighbors_sorted):
                # reversed() because we pop from the stack (LIFO) so if we want to expand
                # in ascending order, we push in descending order
                if nbr not in visited:
                    new_path = path_so_far + [nbr]
                    stack.append((nbr, new_path))

    # If stack is empty, no path exists
    return None, [], nodes_created


def main():
    """
    Main function:
      - Expects 2 arguments: filename and method (e.g., DFS)
      - Parses the file
      - Performs DFS if method == "DFS"
      - Prints result in the required format:
        filename method
        goal number_of_nodes
        path
    """

    if len(sys.argv) != 3:
        print("Usage: python dfs_search.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method   = sys.argv[2]

    # For this example, we only implement DFS.
    if method.upper() != "DFS":
        print(f"Method '{method}' not implemented in this script. Only 'DFS' is supported.")
        sys.exit(1)

    # Parse the file into a graph structure
    graph, origin, destinations = parse_file(filename)

    # Run DFS
    goal, path, num_nodes = dfs_search(graph, origin, destinations)

    # Print output in the required format
    print(f"{filename} {method}")
    if goal:
        print(f"{goal} {num_nodes}")
        print(" ".join(path))
    else:
        print(f"NoGoalFound {num_nodes}")
        print("NoPath")

if __name__ == "__main__":
    main()
