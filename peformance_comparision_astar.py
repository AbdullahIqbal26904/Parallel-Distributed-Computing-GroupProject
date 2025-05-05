import time
import matplotlib.pyplot as plt
from core.maze_utils import generate_maze
from core.maze_utils import createNodes, createFriendsList
from algorithms.a_star import A_star_Search
from algorithms.parallel_astar import parallel_a_star
from visuals.draw import Draw

def a_star_performance_test(sizes=None, num_trials=3, wall_density=0.2):
    """
    Run performance tests comparing sequential and parallel A* algorithms
    on mazes of increasing sizes.
    
    Args:
        sizes: List of (width, height) tuples for maze sizes
        num_trials: Number of trials to run for each size (results will be averaged)
        wall_density: Density of walls in the generated mazes
        
    Returns:
        Dictionary with test results
    """
    if sizes is None:
        # Use larger mazes to better highlight parallel benefits
        sizes = [(20, 20), (30, 30), (40, 40), (60, 60), (80, 80)]
    
    # Initialize results dictionary
    results = {
        'maze_sizes': [],
        'sequential_times': [],
        'parallel_times': [],
        'sequential_nodes': [],
        'parallel_nodes': [],
        'speedup': []
    }
    
    # Create dummy visualization objects (not actually used for timing tests)
    path = Draw("B")
    finalPath = Draw("F")
    goal_pen = Draw("G")
    
    # Run tests for each maze size
    for width, height in sizes:
        print(f"\nTesting maze size: {width}x{height}")
        size_sequential_times = []
        size_parallel_times = []
        size_sequential_nodes = []
        size_parallel_nodes = []
        
        for trial in range(num_trials):
            print(f"  Trial {trial+1}/{num_trials}...")
            
            # Generate random maze
            maze_list = generate_maze(width, height, wall_density)
            
            # Setup maze nodes and graph
            nodes = createNodes(maze_list)
            start, goal, edge_list = createFriendsList(nodes)
            
            # If path generation failed, try again
            if start is None or goal is None:
                print("  Invalid maze generated, retrying...")
                continue
                
            print(f"  Start node at ({start.row}, {start.col}), Goal at ({goal.row}, {goal.col})")
            
            # Create copies of required objects to avoid interference between runs
            # This is especially important for A* which modifies the nodes
            sequential_nodes = createNodes(maze_list)
            sequential_start, sequential_goal, _ = createFriendsList(sequential_nodes)
            
            parallel_nodes = createNodes(maze_list)
            parallel_start, parallel_goal, _ = createFriendsList(parallel_nodes)
            
            # Run sequential A*
            # Note: We need to modify the sequential A* function to return timing info
            # For now, we'll time it externally
            sequential_start_time = time.time()
            try:
                # The original A_star_Search doesn't return path, so we'll handle that
                # by catching exceptions and recording known results
                A_star_Search(sequential_start, sequential_goal, sequential_nodes, path, finalPath, goal_pen)
                # Count path nodes by following parent pointers from goal
                path_nodes = []
                current = sequential_goal
                while current is not None:
                    path_nodes.append(current)
                    current = current.parent
                sequential_path = path_nodes[::-1]  # Reverse to get start-to-goal
            except Exception as e:
                print(f"  Sequential A* error: {e}")
                sequential_path = []
            
            sequential_time = time.time() - sequential_start_time
            size_sequential_times.append(sequential_time)
            size_sequential_nodes.append(len(sequential_path) if sequential_path else 0)
            
            # Run parallel A*
            parallel_start_time = time.time()
            try:
                parallel_path, nodes_processed = parallel_a_star(
                    parallel_start, parallel_goal, parallel_nodes, maze_list, path, finalPath, goal_pen
                )
            except Exception as e:
                print(f"  Parallel A* error: {e}")
                parallel_path = []
                nodes_processed = 0
            
            parallel_time = time.time() - parallel_start_time
            size_parallel_times.append(parallel_time)
            size_parallel_nodes.append(len(parallel_path) if parallel_path else 0)
            
            print(f"  Sequential: {sequential_time:.4f}s, Parallel: {parallel_time:.4f}s")
            if parallel_time > 0:
                print(f"  Speedup: {sequential_time/parallel_time:.2f}x")
            
        # Calculate averages and add to results
        if size_sequential_times and size_parallel_times:
            avg_sequential = sum(size_sequential_times) / len(size_sequential_times)
            avg_parallel = sum(size_parallel_times) / len(size_parallel_times)
            avg_sequential_nodes = sum(size_sequential_nodes) / len(size_sequential_nodes)
            avg_parallel_nodes = sum(size_parallel_nodes) / len(size_parallel_nodes)
            
            results['maze_sizes'].append(f"{width}x{height}")
            results['sequential_times'].append(avg_sequential)
            results['parallel_times'].append(avg_parallel)
            results['sequential_nodes'].append(avg_sequential_nodes)
            results['parallel_nodes'].append(avg_parallel_nodes)
            results['speedup'].append(avg_sequential / avg_parallel if avg_parallel > 0 else 0)
            
            print(f"Average - Sequential: {avg_sequential:.4f}s, Parallel: {avg_parallel:.4f}s")
            if avg_parallel > 0:
                print(f"Average speedup: {avg_sequential/avg_parallel:.2f}x")
    
    # Plot results
    plot_results(results)
    
    return results

def plot_results(results):
    """Plot the performance comparison results."""
    plt.figure(figsize=(12, 10))
    
    # Plot 1: Execution times
    plt.subplot(2, 1, 1)
    plt.plot(results['maze_sizes'], results['sequential_times'], 'b-o', label='Sequential A*')
    plt.plot(results['maze_sizes'], results['parallel_times'], 'r-o', label='Parallel A*')
    plt.xlabel('Maze Size')
    plt.ylabel('Execution Time (seconds)')
    plt.title('A* Algorithm Performance Comparison')
    plt.legend()
    plt.grid(True)
    
    # Plot 2: Speedup
    plt.subplot(2, 1, 2)
    plt.plot(results['maze_sizes'], results['speedup'], 'g-o')
    plt.xlabel('Maze Size')
    plt.ylabel('Speedup (Sequential/Parallel)')
    plt.title('Parallel A* Speedup')
    plt.axhline(y=1, color='r', linestyle='--', label='Equal Performance')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('astar_performance_comparison.png')
    plt.show()

def modified_a_star_search(start, goal, nodes, original_maze=None, path=None, finalPath=None, goal_pen=None):
    """A wrapper for the sequential A* to return the path and timing info"""
    from core.priority_queue import PriorityQueue
    import math
    
    # Heuristic function (Euclidean distance)
    def heuristic(x, y, goal):
        a = math.pow((goal.x - x), 2)
        b = math.pow((goal.y - y), 2)
        return math.sqrt(a + b)
    
    # Reset costs
    for node in nodes:
        node.g_cost = float('inf')
        node.h_cost = float('inf')
        node.parent = None
    
    start.g_cost = 0
    start.h_cost = heuristic(start.x, start.y, goal)
    
    # Initialize data structures
    queue = PriorityQueue()
    queue.put(start, start.f_cost())
    visited = set()
    
    nodes_explored = 0
    while not queue.is_empty():
        current = queue.get()
        nodes_explored += 1
        
        if current in visited:
            continue
        visited.add(current)
        
        if current == goal:
            break
            
        for neighbor in current.friend:
            if neighbor.data == "X" or neighbor in visited:
                continue
                
            tentative_g = current.g_cost + 20  # Edge cost
            
            if tentative_g < neighbor.g_cost:
                neighbor.parent = current
                neighbor.g_cost = tentative_g
                neighbor.h_cost = heuristic(neighbor.x, neighbor.y, goal)
                queue.put(neighbor, neighbor.f_cost())
    
    # Reconstruct path
    path_list = []
    current_node = goal
    while current_node is not None:
        path_list.append(current_node)
        current_node = current_node.parent
    path_list.reverse()
    
    return path_list, nodes_explored

if __name__ == "__main__":
    # Define maze sizes to test: (width, height)
    # Use slightly larger mazes to better see the parallel performance difference
    sizes = [(10,10), (20, 20), (30, 30), (40, 40), (50, 50)]
    
    # Larger wall density will create more complex mazes
    wall_density = 0.25
    
    # Run the performance test with 3 trials per maze size
    a_star_performance_test(sizes=sizes, num_trials=3, wall_density=wall_density)