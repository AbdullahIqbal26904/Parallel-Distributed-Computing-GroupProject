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
    """Process nodes in a bucket. Uses global shared memory variables."""
    nodes_to_process, bucket_idx = args
    local_relaxed_edges = []
    found_goal = False

    for node in nodes_to_process:
        # Get current cost from shared array
        with global_costs.get_lock():
            current_cost = global_costs[node.id]

        # Skip processing if a lower cost was found by another process
        with global_visited.get_lock():
            if global_visited[node.id]:
                continue

        with global_nodes_explored.get_lock():
            global_nodes_explored.value += 1

        if node.id == global_goal_id:
            return [], True

        # Process all edges
        for neighbor in node.friend:
            if neighbor.data == "X":
                continue

            weight = 20  # Fixed edge weight
            new_cost = current_cost + weight
            neighbor_id = neighbor.id

            # Update cost and parent if better path found
            with global_costs.get_lock():
                if new_cost < global_costs[neighbor_id]:
                    global_costs[neighbor_id] = new_cost
                    with global_parents.get_lock():
                        global_parents[neighbor_id] = node.id
                    new_bucket = int(new_cost // global_delta)
                    local_relaxed_edges.append((neighbor, new_bucket))

        # Mark node as visited
        with global_visited.get_lock():
            global_visited[node.id] = 1

    return local_relaxed_edges, found_goal

def parallel_process_bucket(current_bucket, buckets, costs, parents, visited, goal_id, delta, nodes_explored, num_processes):
    """Process a bucket in parallel using a pool of workers."""
    if not buckets[current_bucket]:
        return [], False

    nodes_per_process = max(1, len(buckets[current_bucket]) // num_processes)
    node_chunks = [buckets[current_bucket][i:i + nodes_per_process] 
                   for i in range(0, len(buckets[current_bucket]), nodes_per_process)]
    args = [(chunk, current_bucket) for chunk in node_chunks]

    # Initialize pool with shared memory variables
    with mp.Pool(
        processes=min(num_processes, len(node_chunks)),
        initializer=init_worker,
        initargs=(costs, parents, visited, goal_id, delta, nodes_explored)
    ) as pool:
        results = pool.map(process_bucket_nodes, args)

    all_relaxed_edges = []
    goal_found = False
    for relaxed_edges, found_goal in results:
        all_relaxed_edges.extend(relaxed_edges)
        if found_goal:
            goal_found = True
    return all_relaxed_edges, goal_found

def delta_stepping_dijkstra(start, goal, nodes, original_maze, path, finalPath, goal_pen, num_processes=None, delta=20):
    """Delta-Stepping Parallel Dijkstra's algorithm using shared memory."""
    if num_processes is None:
        num_processes = mp.cpu_count()

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
    costs = mp.Array('d', num_nodes, lock=True)
    parents = mp.Array('i', num_nodes, lock=True)
    visited = mp.Array('b', num_nodes, lock=True)

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

    current_bucket = 0
    while current_bucket < 1000:  # Prevent infinite loops
        if not buckets[current_bucket]:
            current_bucket += 1
            continue

        # Process current bucket in parallel
        relaxed_edges, goal_found = parallel_process_bucket(
            current_bucket, buckets, costs, parents, visited, goal_id, delta, nodes_explored, num_processes
        )

        if goal_found:
            break

        # Update buckets with relaxed edges
        for node, bucket_idx in relaxed_edges:
            if node not in buckets[bucket_idx]:
                buckets[bucket_idx].append(node)

        buckets[current_bucket].clear()
        current_bucket += 1

    # Update node attributes from shared memory
    for node in nodes:
        node.g_cost = costs[node.id]
        parent_id = parents[node.id]
        node.parent = nodes[parent_id] if parent_id != -1 else None

    # Calculate results
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Delta-Stepping search completed in {execution_time:.4f} seconds")
    print(f"Nodes explored: {nodes_explored.value}")

    # Reconstruct path
    final_path = []
    if visited[goal_id] or costs[goal_id] < float('inf'):
        current = goal
        while current is not None:
            final_path.append(current)
            current = current.parent
        final_path.reverse()
        print(f"Path found with {len(final_path)} steps")
    else:
        print("No path found!")

    return final_path, execution_time, nodes_explored.value