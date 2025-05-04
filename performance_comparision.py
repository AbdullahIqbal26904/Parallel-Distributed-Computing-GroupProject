import time
import matplotlib.pyplot as plt
from core.maze_utils import generate_maze
from core.maze_utils import createNodes, createFriendsList
from algorithms.dijkstra import dijkstra_search
from algorithms.parallel_dijkstra import delta_stepping_dijkstra
from visuals.draw import Draw

def performance_test(sizes=None, num_trials=3, wall_density=0.2, num_processes=8, delta=20):
    """
    Run performance tests comparing sequential and parallel Dijkstra algorithms
    on mazes of increasing sizes.
    
    Args:
        sizes: List of (width, height) tuples for maze sizes
        num_trials: Number of trials to run for each size (results will be averaged)
        wall_density: Density of walls in the generated mazes
        num_processes: Number of processes for parallel algorithm (None for auto)
        delta: Delta parameter for parallel Dijkstra
        
    Returns:
        Dictionary with test results
    """
    if sizes is None:
        sizes = [(10, 10), (20, 20), (30, 30), (40, 40), (50, 50)]
    
    # Initialize results dictionary
    results = {
        'maze_sizes': [],
        'sequential_times': [],
        'parallel_times': [],
        'sequential_nodes': [],
        'parallel_nodes': [],
        'speedup': []
    }
    
    # Create dummy visualization objects (not actually used)
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
            # print(maze_list)
            # Setup maze nodes and graph
            nodes = createNodes(maze_list)
            start, goal, edge_list = createFriendsList(nodes)
            
            # If path generation failed, try again
            if start is None or goal is None:
                print("  Invalid maze generated, retrying...")
                continue
                
            print(f"  Start node at ({start.row}, {start.col}), Goal at ({goal.row}, {goal.col})")
            
            # Run sequential Dijkstra
            sequential_start = time.time()
            sequential_path = dijkstra_search(start, goal, nodes, maze_list, path, finalPath, goal_pen)
            sequential_time = time.time() - sequential_start
            size_sequential_times.append(sequential_time)
            size_sequential_nodes.append(len(sequential_path) if sequential_path else 0)
            
            # Reset node costs
            for node in nodes:
                node.g_cost = float('inf')
                node.parent = None
            start.g_cost = 0
            
            # Run parallel Dijkstra
            final_path, parallel_time, _ = delta_stepping_dijkstra(start, goal, nodes, maze_list, path, finalPath, goal_pen, num_processes, delta)
            size_parallel_times.append(parallel_time)
            size_parallel_nodes.append(len(final_path) if final_path else 0)
            
            print(f"  Sequential: {sequential_time:.4f}s, Parallel: {parallel_time:.4f}s")
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
            print(f"Average speedup: {avg_sequential/avg_parallel:.2f}x")
    
    # Plot results
    plot_results(results)
    
    return results

def plot_results(results):
    """Plot the performance comparison results."""
    plt.figure(figsize=(12, 10))
    
    # Plot 1: Execution times
    plt.subplot(2, 1, 1)
    plt.plot(results['maze_sizes'], results['sequential_times'], 'b-o', label='Sequential Dijkstra')
    plt.plot(results['maze_sizes'], results['parallel_times'], 'r-o', label='Parallel Dijkstra')
    plt.xlabel('Maze Size')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Dijkstra Algorithm Performance Comparison')
    plt.legend()
    plt.grid(True)
    
    # Plot 2: Speedup
    plt.subplot(2, 1, 2)
    plt.plot(results['maze_sizes'], results['speedup'], 'g-o')
    plt.xlabel('Maze Size')
    plt.ylabel('Speedup (Sequential/Parallel)')
    plt.title('Parallel Speedup')
    plt.axhline(y=1, color='r', linestyle='--', label='Equal Performance')
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('dijkstra_performance_comparison.png')
    plt.show()

if __name__ == "__main__":
    # Define maze sizes to test: (width, height)
    sizes = [(10, 10), (20, 20), (30, 30), (40, 40), (50, 50)]
    
    # Run the performance test
    performance_test(sizes=sizes, num_trials=3)