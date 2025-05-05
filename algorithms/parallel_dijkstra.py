import time
import multiprocessing as mp
from collections import defaultdict
import sys
sys.setrecursionlimit(10000)

# Global variables for shared memory in worker processes
global_costs = None
global_parents = None
global_visited = None
global_goal_id = None
global_delta = None
global_nodes_explored = None

def init_worker(costs, parents, visited, goal_id, delta, nodes_explored):
    """Initializer function to set up global variables in each worker process."""
    global global_costs, global_parents, global_visited, global_goal_id, global_delta, global_nodes_explored
    global_costs = costs
    global_parents = parents
    global_visited = visited
    global_goal_id = goal_id
    global_delta = delta
    global_nodes_explored = nodes_explored

def process_bucket_nodes(args):
    """Process nodes in a bucket with reduced lock contention."""
    nodes_to_process, bucket_idx = args
    local_relaxed_edges = []
    found_goal = False
    local_nodes_explored = 0
    
    # Get values once with lock to minimize contention
    with global_costs.get_lock():
        local_costs = {node.id: global_costs[node.id] for node in nodes_to_process}
    
    # Collect local updates to apply later in batch
    local_cost_updates = {}
    local_parent_updates = {}
    
    for node in nodes_to_process:
        current_cost = local_costs[node.id]
        local_nodes_explored += 1
        
        if node.id == global_goal_id:
            found_goal = True
            continue
        
        # Process all neighbors without locks
        for neighbor in node.friend:
            if neighbor.data == "X":
                continue
                
            weight = 20  # Standard edge weight
            new_cost = current_cost + weight
            
            # Store updates locally without locks
            if neighbor.id not in local_cost_updates or new_cost < local_cost_updates[neighbor.id]:
                local_cost_updates[neighbor.id] = new_cost
                local_parent_updates[neighbor.id] = node.id
                new_bucket = int(new_cost // global_delta)
                local_relaxed_edges.append((neighbor, new_bucket))
    
    # Now apply updates with minimal lock acquisitions
    nodes_to_visit = set(node.id for node in nodes_to_process)
    
    # Update costs in a single lock acquisition
    if local_cost_updates:
        with global_costs.get_lock():
            for n_id, n_cost in local_cost_updates.items():
                if n_cost < global_costs[n_id]:
                    global_costs[n_id] = n_cost
                    global_parents[n_id] = local_parent_updates.get(n_id)
                else:
                    # Remove from relaxed edges if we didn't actually improve
                    local_relaxed_edges = [(n, b) for n, b in local_relaxed_edges if n.id != n_id]
    
    # Mark visited all at once
    with global_visited.get_lock():
        for node_id in nodes_to_visit:
            global_visited[node_id] = 1
    
    # Update nodes explored counter once
    with global_nodes_explored.get_lock():
        global_nodes_explored.value += local_nodes_explored

    return local_relaxed_edges, found_goal

def delta_stepping_dijkstra(start, goal, nodes, original_maze, path, finalPath, goal_pen, num_processes=None, delta=20):
    """Delta-Stepping Parallel Dijkstra's algorithm using shared memory with reduced overhead."""
    # Auto-configure number of processes
    if num_processes is None:
        num_processes = max(1, mp.cpu_count() - 1)  # Leave one core free for system
    
    # Adjust delta based on maze size for better parallelization
    if delta <= 0:
        delta = max(20, len(nodes) // 100)
    
    print(f"Running parallel Dijkstra with {num_processes} processes, delta={delta}")

    # Reset node attributes
    for node in nodes:
        node.g_cost = float('inf')
        node.parent = None
    start.g_cost = 0

    # Assign unique IDs to nodes
    num_nodes = len(nodes)
    for idx, node in enumerate(nodes):
        node.id = idx

    # Create shared memory arrays
    costs = mp.Array('d', num_nodes)
    parents = mp.Array('i', num_nodes)
    visited = mp.Array('b', num_nodes)

    # Initialize shared arrays
    for i in range(num_nodes):
        costs[i] = float('inf')
        parents[i] = -1
        visited[i] = 0

    start_id = start.id
    costs[start_id] = 0.0
    goal_id = goal.id

    # Organize nodes into buckets
    buckets = defaultdict(list)
    buckets[0].append(start)

    # Track exploration
    start_time = time.time()
    nodes_explored = mp.Value('i', 0)

    # Use context manager to ensure proper cleanup
    with mp.Pool(
        processes=num_processes,
        initializer=init_worker,
        initargs=(costs, parents, visited, goal_id, delta, nodes_explored)
    ) as pool:
        current_bucket = 0
        max_bucket = 1000  # Reasonable upper limit
        goal_found = False
        
        while current_bucket <= max_bucket and not goal_found:
            if not buckets[current_bucket]:
                current_bucket += 1
                continue

            # Optimize chunk size based on problem size
            total_nodes = len(buckets[current_bucket])
            chunk_size = max(1, min(50, total_nodes // (num_processes * 2))) 
            
            # Create chunks with reasonable size
            node_chunks = []
            for i in range(0, total_nodes, chunk_size):
                chunk = buckets[current_bucket][i:i + chunk_size]
                if chunk:  # Only add non-empty chunks
                    node_chunks.append(chunk)
            
            args = [(chunk, current_bucket) for chunk in node_chunks]
            if not args:
                current_bucket += 1
                continue
                
            # Process all chunks in parallel
            results = pool.map(process_bucket_nodes, args)

            # Process results
            all_relaxed_edges = []
            for relaxed_edges, found_goal in results:
                all_relaxed_edges.extend(relaxed_edges)
                if found_goal:
                    goal_found = True
            
            if goal_found:
                break

            # Add relaxed edges to buckets, avoiding duplicates efficiently
            bucket_node_map = {}  # Track nodes already in buckets
            for node, bucket_idx in all_relaxed_edges:
                max_bucket = max(max_bucket, bucket_idx)
                
                # Only add each node to a bucket once per iteration
                node_key = (node.id, bucket_idx)
                if node_key not in bucket_node_map:
                    bucket_node_map[node_key] = True
                    buckets[bucket_idx].append(node)

            # Clear the current bucket after processing
            buckets[current_bucket].clear()
            current_bucket += 1

    # Calculate results
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Delta-Stepping search completed in {execution_time:.4f} seconds")
    print(f"Nodes explored: {nodes_explored.value}")

    # Update node attributes from shared memory
    for i, node in enumerate(nodes):
        node.g_cost = costs[i]
        parent_id = parents[i]
        if parent_id >= 0 and parent_id < len(nodes):
            node.parent = nodes[parent_id]
        else:
            node.parent = None

    # Reconstruct path
    final_path = []
    current = goal
    if visited[goal_id] or costs[goal_id] < float('inf'):
        while current is not None:
            final_path.append(current)
            current = current.parent
        final_path.reverse()
        print(f"Path found with {len(final_path)} steps")
    else:
        print("No path found!")

    # Make sure to finish the function properly
    return final_path, execution_time, nodes_explored.value