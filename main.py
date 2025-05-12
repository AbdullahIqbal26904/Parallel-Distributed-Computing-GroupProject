from visuals.draw import Draw
from visuals.draw import reset_maze
from visuals.draw import setup_maze
import turtle
from core.maze_utils import read_File_Create_List
from core.maze_utils import createNodes
from core.maze_utils import createFriendsList
from algorithms.a_star import A_star_Search
from algorithms.dijkstra import dijkstra_search
# Import the parallel implementation
from algorithms.parallel_dijkstra import delta_stepping_dijkstra
from algorithms.parallel_astar import parallel_a_star
import time
# Add to imports at top
# from algorithms.delta_stepping_dijkstra import delta_stepping_dijkstra
def print_maze_with_path(maze_list, path_nodes):
    """Print the maze with the final path marked with 'P'"""
    # Create a copy of the maze to avoid modifying the original
    maze_copy = [row[:] for row in maze_list]
    
    # Mark the path on the maze copy
    for node in path_nodes:
        # Skip marking start and goal positions to keep them visible
        if maze_copy[node.row][node.col] not in ['p', 'g']:
            maze_copy[node.row][node.col] = 'F'  # 'P' represents path
    
    # Print the maze with path
    print("\nMaze with final path:")
    for row in maze_copy:
        print(''.join(row))

def dijkstra_performance_test(root, goal_node, n, maze_list, path, finalPath, goal_pen, num_processes, delta):
    # run sequential
    pass

if __name__ == '__main__':
    user_input = int(input(
        "Enter 1 for A*, 2 for Dijkstra, 3 for Bellman-Ford, 4 for Parallel Dijkstra: ," \
        "5 for Parallel A*"))
    filename = "maze.txt"
    print(filename)
    Wall = Draw("W")
    Start = Draw("p")
    goal_pen = Draw("G")
    path = Draw("B")
    finalPath = Draw("F")
    pen_for_pheromone = Draw("pheromone")
    
    maze_list = read_File_Create_List(filename)
    n = createNodes(maze_list)
    root, goal_node, edge_list = createFriendsList(n)
    # wn.onkey(lambda: reset_maze(path, finalPath), 'r')

    if user_input == 1:
        wn = turtle.Screen()
        wn.bgcolor("black")
        wn.title("Maze Solver")
        wn.setup(1400, 800)
        setup_maze(maze_list, Wall, Start, goal_pen)
        A_star_Search(root, goal_node, n, path, finalPath, goal_pen)
        wn.mainloop()
    elif user_input == 2:
        wn = turtle.Screen()
        wn.bgcolor("black")
        wn.title("Maze Solver")
        wn.setup(1400, 800)
        setup_maze(maze_list, Wall, Start, goal_pen)
        
        dijkstra_search(root, goal_node, n, maze_list, path, finalPath, goal_pen)
        wn.mainloop()
    elif user_input == 3:
        pass
        # setup_maze(maze_list, Wall, Start, goal_pen)
        # bellman_ford_search(root, goal_node, n, edge_list, maze_list,
        #                     path, finalPath, goal_pen)
    elif user_input == 4:
        # Run Delta-Stepping Dijkstra
        num_processes = int(input("Enter number of processes (or 0 for auto): ") or "0")
        delta = int(input("Enter delta value (or 0 for default): ") or "0")
        if num_processes <= 0:
            num_processes = None
        if delta <= 0:
            delta = 20  # Default delta value
        # setup_maze(maze_list, Wall, Start, goal_pen)
        final_path, execution_time, _ = delta_stepping_dijkstra(root, goal_node, n, maze_list, path, finalPath, goal_pen, num_processes, delta)
        print(f"Execution time: {execution_time:.2f} seconds")
        print("Final path coordinates:")
        for node in final_path:
            print(f"  ({node.row}, {node.col}) at position ({node.x}, {node.y})")
        
        # Print the maze with the path marked
        print_maze_with_path(maze_list, final_path)
# In your main function:
        # Update the section that calls parallel_a_star:
    
    elif user_input == 5:
        # setup_maze(maze_list, Wall, Start, goal_pen)
        start_time = time.time()
        final_path, nodes_processed = parallel_a_star(root, goal_node, n, maze_list, path, finalPath, goal_pen)
        execution_time = time.time() - start_time
        
        print(f"Parallel A* search completed in {execution_time:.4f} seconds")
        print(f"Nodes processed: {nodes_processed}")
        
        if final_path:
            print(f"Path found with {len(final_path)} steps")
            # Path is already visualized in the function
            
            # Print the maze with the path marked
            # print_maze_with_path(maze_list, final_path)
        else:
            print("No path found!")
    elif user_input == 6:
        print("Running Parallel Dijkstra...")
    