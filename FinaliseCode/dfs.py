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
            for (node, _) in reversed(neighbors_sorted):
                if node not in visited:
                    new_path = path_so_far + [node]
                    stack.append((node, new_path))

    return None, [], nodes_created
