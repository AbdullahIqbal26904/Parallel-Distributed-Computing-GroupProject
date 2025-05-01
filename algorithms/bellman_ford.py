from visuals.draw import display_maze_with_path

import time


def bellman_ford_search(start, goal, nodes, edges, original_maze, path, finalPath, goal_pen):
    # Reset costs and parents
    for node in nodes:
        node.g_cost = float('inf')
        node.parent = None
    start.g_cost = 0  # Initialize start node

    # Track visited nodes for visualization
    visited_nodes = set()

    # Main Bellman-Ford loop with early termination
    for _ in range(len(nodes) - 1):
        updated = False
        goal_found = False  # Flag to check if goal is reached

        for u, v, w in edges:
            # Skip edges involving walls (already excluded in edge creation)
            if u.data == "X" or v.data == "X":
                continue

            # Relaxation step
            if u.g_cost + w < v.g_cost:
                v.g_cost = u.g_cost + w
                v.parent = u
                updated = True

                # Visualize exploration
                if v not in visited_nodes and v.data not in ('p', 'G'):
                    path.goto(v.x, v.y)
                    path.stamp()
                    visited_nodes.add(v)
                    time.sleep(0.05)

                # Check if goal is reached
                if v == goal and v.g_cost != float('inf'):
                    goal_found = True  # Set flag to break outer loops

        # Early termination checks
        if not updated:
            break  # No more improvements possible
        if goal_found:
            break  # Goal reached, exit early

    # Validate and reconstruct path
    if goal.g_cost == float('inf'):
        print("No valid path exists.")
        return

    # Reconstruct path from goal to start
    path_list = []
    current = goal
    while current is not None:
        path_list.append(current)
        current = current.parent
    path_list.reverse()

    # Draw final path (ensure no walls)
    for node in path_list:
        if node.data in ('p', 'G'):
            continue
        if node.data == "X":
            print("Error: Path includes a wall. Maze invalid.")
            return
        finalPath.goto(node.x, node.y)
        finalPath.stamp()
        time.sleep(0.1)

    display_maze_with_path(original_maze, path_list)
    goal_pen.color("red")
    goal_pen.goto(goal.x, goal.y)
    goal_pen.stamp()
