from core.priority_queue import PriorityQueue
import math
import time
import multiprocessing as mp
from visuals.draw import setup_maze, Draw

def heuristic(x, y, goal):
    # Manhattan distance may work better for grid-based mazes
    return abs(goal.x - x) + abs(goal.y - y)
    # Or Euclidean distance
    # return math.sqrt((goal.x - x)**2 + (goal.y - y)**2)

def process_neighbors(current_node, neighbors_chunk, goal, visited, parent, g_costs):
    """Parallel processing of neighbors for a single node"""
    results = []
    
    for neighbor in neighbors_chunk:
        # Skip walls and already visited nodes
        if neighbor.data == "X" or visited[neighbor.id]:
            continue
            
        # Calculate costs
        new_g = current_node.g_cost + 20  # Fixed edge weight
        new_h = heuristic(neighbor.x, neighbor.y, goal)
        new_f = new_g + new_h
        
        # Only consider this neighbor if we've found a better path
        if new_g < g_costs[neighbor.id]:
            results.append((neighbor, new_g, new_h, new_f, current_node.id))
        
    return results


def parallel_a_star(start, goal, nodes, original_maze=None, path=None, finalPath=None, goal_pen=None):
    # Initialize nodes with IDs
    for idx, node in enumerate(nodes):
        node.id = idx
        node.g_cost = float('inf')
        node.h_cost = 0
    
    # Set start node cost
    start.g_cost = 0
    
    # Print debug info
    print(f"Start node: ID={start.id}, pos=({start.x}, {start.y})")
    print(f"Goal node: ID={goal.id}, pos=({goal.x}, {goal.y})")
    
    # Shared memory arrays with Manager
    manager = mp.Manager()
    visited = manager.list([0] * len(nodes))
    parent = manager.list([-1] * len(nodes))
    g_costs = manager.list([float('inf')] * len(nodes))
    g_costs[start.id] = 0
    
    # Priority queue in main process
    queue = PriorityQueue()
    start_f = heuristic(start.x, start.y, goal)
    queue.put(start, start_f)
    visited[start.id] = 1
    
    # Process pool
    num_processes = mp.cpu_count()
    print(f"Using {num_processes} processes for parallel processing")
    pool = mp.Pool(processes=num_processes)
    
    goal_found = False
    nodes_processed = 0
    
    while not queue.is_empty() and not goal_found:
        current_node = queue.get()
        nodes_processed += 1
        
        if nodes_processed % 10 == 0:
            print(f"Processed {nodes_processed} nodes. Queue size: {len(queue.elements)}")
        
        # Check if we've reached the goal
        if current_node.id == goal.id:
            print(f"Goal found at node {current_node.id}!")
            goal_found = True
            break
            
        # Skip if we already found a better path to this node
        if current_node.g_cost > g_costs[current_node.id]:
            continue
            
        # Split neighbors into chunks for parallel processing
        neighbors = [n for n in current_node.friend if n.data != "X"]
        if not neighbors:
            continue
            
        chunk_size = max(1, len(neighbors) // num_processes)
        chunks = [neighbors[i:i+chunk_size] for i in range(0, len(neighbors), chunk_size)]
        
        # Process neighbors in parallel
        args = [(current_node, chunk, goal, visited, parent, g_costs) for chunk in chunks]
        results = pool.starmap(process_neighbors, args)
        
        # Update queue and shared data structures
        for chunk_results in results:
            for neighbor, new_g, new_h, new_f, parent_id in chunk_results:
                # Update costs atomically
                if new_g < g_costs[neighbor.id]:
                    g_costs[neighbor.id] = new_g
                    parent[neighbor.id] = parent_id
                    
                    # Only add to queue if not visited
                    if not visited[neighbor.id]:
                        visited[neighbor.id] = 1
                        queue.put(neighbor, new_f)
                        
                        # Update the node's costs for visualization purposes
                        neighbor.g_cost = new_g
                        neighbor.h_cost = new_h
                        
                        # Check if we're adding the goal to the queue
                        if neighbor.id == goal.id:
                            print(f"Added goal to queue with f-cost: {new_f}")

    pool.close()
    pool.join()
    
    # Debugging: check goal status
    print(f"Goal node (ID: {goal.id}) final status:")
    print(f"  Visited: {bool(visited[goal.id])}")
    print(f"  Cost: {g_costs[goal.id]}")
    print(f"  Parent: {parent[goal.id]}")
    
    # Reconstruct path
    path = []
    if goal_found or visited[goal.id]:
        current_id = goal.id
        while current_id != -1:
            path.append(nodes[current_id])
            current_id = parent[current_id]
        path.reverse()
        
        print(f"Path found with {len(path)} steps")
        
        # Visualize path if visualization tools are provided
        if finalPath and original_maze:
            for node in path:
                if node.data not in ['p', 'G']:
                    finalPath.goto(node.x, node.y)
                    finalPath.stamp()
    else:
        print("No path found to goal!")
        
    return path, nodes_processed