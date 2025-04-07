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

    # part currently being read
    section = None

    for line in lines:
        line = line.strip()

        if not line:
            continue  
        
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
            node_part, coord_part = line.split(':')
            node_id = node_part.strip()
            # coords in the form (x,y)
            _coords = coord_part.strip()

            # Initialize adjacency list for this node if not present
            if node_id not in graph:
                graph[node_id] = []

        elif section == "edges":
            # line: (2,1): 4
            edge_part, cost_part = line.split(':')
            edge_part = edge_part.strip()  # e.g. (2,1)
            cost = cost_part.strip()       # e.g. 4

            edge_part = edge_part.replace('(', '').replace(')', '')
            start_node, end_node = edge_part.split(',')
            start_node = start_node.strip()
            end_node   = end_node.strip()

            if start_node not in graph:
                graph[start_node] = []
            graph[start_node].append((end_node, float(cost)))

        elif section == "origin":
            # single line, e.g. 2
            origin = line.strip()

        elif section == "destinations":
            # may be multiple destinations, e.g. 5; 4
            # e.g. 5; 4
            parts = line.split(';')
            for p in parts:
                dest = p.strip()
                if dest:
                    destinations.append(dest)

    return graph, origin, destinations


def dfs_search(graph, origin, destinations):
    # We'll use a stack for DFS. Each item on the stack is a tuple:
    # graph is a dict
    # tuple: (current_node, path_to_here)

    stack = [(origin, [origin])]
    visited = set()        # nodes visited so far
    nodes_created = 0      # how many nodes we've generated so far

    while stack:
        current_node, path_so_far = stack.pop()
        nodes_created += 1  # take the node off stack, upon expansion

        # if destination found, return it
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

    if len(sys.argv) != 3:
        print("Usage: python dfs_search.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method   = sys.argv[2]

    # For now, dfs only
    if method.upper() != "DFS":
        print(f"Method '{method}' not implemented in this script. Only 'DFS' is supported.")
        sys.exit(1)

    # Parse into graph structure
    graph, origin, destinations = parse_file(filename)

    # Run DFS
    goal, path, num_nodes = dfs_search(graph, origin, destinations)

    # Print output
    print(f"{filename} {method}")
    if goal:
        print(f"{goal} {num_nodes}")
        print(" ".join(path))
    else:
        print(f"NoGoalFound {num_nodes}")
        print("NoPath")

if __name__ == "__main__":
    main()
