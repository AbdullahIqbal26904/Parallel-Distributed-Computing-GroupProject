from core.priority_queue import PriorityQueue
import time
from visuals.draw import display_maze_with_path


def dijkstra_search(start, goal, mazeList, path, finalPath, goal_pen):
    # Reset costs and parents for all nodes
    for node in mazeList:
        node.g_cost = float('inf')
        node.parent = None
    start.g_cost = 0

    queue = PriorityQueue()
    queue.put(start, start.g_cost)
    visited = set()

    while not queue.is_empty():
        current = queue.get()

        if current in visited:
            continue
        visited.add(current)

        # Visualize exploration
        if current.data not in ('p', 'G'):
            path.goto(current.x, current.y)
            path.stamp()
            time.sleep(0.1)

        if current == goal:
            break

        for neighbor in current.friend:
            if neighbor.data == "X":
                continue  # Skip walls

            tentative_g = current.g_cost + 20  # Edge cost

            if tentative_g < neighbor.g_cost:
                neighbor.g_cost = tentative_g
                neighbor.parent = current
                queue.put(neighbor, neighbor.g_cost)

    # Reconstruct path
    path_list = []
    current_node = goal
    while current_node is not None:
        path_list.append(current_node)
        current_node = current_node.parent
    path_list.reverse()

    # Draw final path
    for node in path_list:
        if node.data not in ('p', 'G'):
            finalPath.goto(node.x, node.y)
            finalPath.stamp()
            time.sleep(0.1)

    display_maze_with_path([row[:] for row in mazeList], path_list)
    goal_pen.color("red")
    goal_pen.goto(goal.x, goal.y)
    goal_pen.stamp()
